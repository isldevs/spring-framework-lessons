#!/usr/bin/env python3
"""Compile and execute actual Spring dependency-resolution tests."""
from pathlib import Path
import hashlib
import json
import subprocess
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
E = ROOT.parent / "evidence"
E.mkdir(exist_ok=True)


def run(command, stem):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    (E / f"java-{stem}.stdout.txt").write_text(result.stdout)
    (E / f"java-{stem}.stderr.txt").write_text(result.stderr)
    (E / f"java-{stem}.exit-code.txt").write_text(str(result.returncode) + "\n")
    (E / f"java-{stem}.command.json").write_text(json.dumps({
        "command": command, "cwd": str(ROOT), "exit_code": result.returncode
    }, indent=2) + "\n")
    if result.returncode:
        raise RuntimeError(f"{stem} failed\n{result.stderr}\n{result.stdout}")
    return result


run(["sha256sum", "-c", "dependencies.sha256"], "dependencies")
classpath = ":".join(str(p.relative_to(ROOT)) for p in sorted((ROOT / "lib").glob("*.jar")))
for folder in ["main", "test", "test-results"]:
    target = ROOT / "build" / folder
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
compiler = ["java", "-jar", "lib/ecj-3.40.0.jar", "-17", "-parameters", "-warn:none"]
main = run([*compiler, "-cp", classpath, "-d", "build/main", *[
    str(p.relative_to(ROOT)) for p in sorted((ROOT / "src/main/java").rglob("*.java"))
]], "compile-main")
tests = run([*compiler, "-cp", "build/main:" + classpath, "-d", "build/test", *[
    str(p.relative_to(ROOT)) for p in sorted((ROOT / "src/test/java").rglob("*.java"))
]], "compile-tests")
# Actual JUnit methods register, refresh and close AnnotationConfigApplicationContext instances.
junit = run([
    "java", "-cp", "build/main:build/test:" + classpath,
    "org.junit.platform.console.ConsoleLauncher", "execute", "--disable-banner",
    "--disable-ansi-colors", "--class-path", "build/main:build/test",
    "--select-class", "lesson.optional.OptionalTest", "--reports-dir",
    "build/test-results", "--details", "tree"
], "junit")
version = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
(E / "java-version.txt").write_text(version.stderr)
reports = []
for path in sorted((ROOT / "build/test-results").glob("TEST-*.xml")):
    attributes = ET.parse(path).getroot().attrib
    reports.append({"file": str(path.relative_to(ROOT)), **attributes})
    (E / ("java-" + path.name)).write_bytes(path.read_bytes())
found = sum(int(float(r.get("tests", "0"))) for r in reports)
failed = sum(int(float(r.get("failures", "0"))) + int(float(r.get("errors", "0"))) for r in reports)
skipped = sum(int(float(r.get("skipped", "0"))) for r in reports)
assert found == 4 and failed == 0 and skipped == 0, reports
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'src').rglob('*.java')}
result={'tests_found':found,'tests_failed':failed,'tests_skipped':skipped,'source_sha256':hashes,'spring':'6.2.11','junit':'5.12.2','proof_lines':[x for x in junit.stdout.splitlines() if x.startswith(('required ','optional ','ambiguity '))],'runtime':version.stderr,'compile_exit':0,'junit_exit':0,'warnings':'Expected negative refresh warnings retained in stderr'}
(E/'java-verification-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(junit.stdout)
