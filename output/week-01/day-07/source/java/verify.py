#!/usr/bin/env python3
"""Compile and execute one actual Spring TestContext/JUnit smoke test."""
from pathlib import Path
import hashlib
import json
import subprocess
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
    (ROOT / "build" / folder).mkdir(parents=True, exist_ok=True)
compiler = ["java", "-jar", "lib/ecj-3.40.0.jar", "-17", "-parameters", "-warn:none"]
main = run([*compiler, "-cp", classpath, "-d", "build/main", *[
    str(p.relative_to(ROOT)) for p in sorted((ROOT / "src/main/java").rglob("*.java"))
]], "compile-main")
tests = run([*compiler, "-cp", "build/main:" + classpath, "-d", "build/test", *[
    str(p.relative_to(ROOT)) for p in sorted((ROOT / "src/test/java").rglob("*.java"))
]], "compile-tests")
# SpringExtension/TestContext loading is genuinely exercised by @SpringJUnitConfig.
junit = run([
    "java", "-cp", "build/main:build/test:" + classpath,
    "org.junit.platform.console.ConsoleLauncher", "execute", "--disable-banner",
    "--disable-ansi-colors", "--class-path", "build/main:build/test",
    "--select-class", "lesson.smoke.ContextSmokeTest", "--reports-dir",
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
assert found == 1 and failed == 0 and skipped == 0, reports
proofs = ["bean found: true", "wiring same: true"]
assert all(line in junit.stdout.splitlines() for line in proofs)
assert "contextLoadsAndWires()" in junit.stdout
hashes = {
    str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted((ROOT / "src").rglob("*.java"))
}
(E / "java-source-hashes.sha256").write_text("".join(v + "  " + k + "\n" for k, v in hashes.items()))
result = {
    "spring_framework_version": "6.2.11", "spring_test_version": "6.2.11",
    "micrometer_version": "1.15.4", "junit_jupiter_version": "5.12.2",
    "junit_platform_version": "1.12.2", "compiler": "ECJ3.40.0",
    "class_file_target": "Java17", "runtime": version.stderr.strip(),
    "compile_main_exit_code": main.returncode, "compile_tests_exit_code": tests.returncode,
    "junit_exit_code": junit.returncode,
    "compile_stderr_empty": not main.stderr and not tests.stderr,
    "junit_stderr_empty": not junit.stderr,
    "application_execution": "Not performed; this lesson verifies the actual JUnit/Spring test execution.",
    "junit_reports": reports, "tests_found": found, "tests_succeeded": found - failed - skipped,
    "tests_failed": failed, "tests_skipped": skipped,
    "proof_lines": [line for line in junit.stdout.splitlines() if line in proofs],
    "test_stdout_proof_lines": proofs, "source_sha256": hashes,
    "context_loading_mechanism": "@SpringJUnitConfig(Config.class) with SpringExtension/TestContext framework",
    "scope": "One real JUnit test loads the selected Config, retrieves OrderService/Repo and checks constructor dependency identity. No business behavior or full-application coverage is inferred.",
    "verified_semantics": {
        "spring_test_context_loads_selected_configuration": True,
        "required_order_service_retrievable": "bean found: true" in junit.stdout.splitlines(),
        "required_repo_retrievable": "wiring same: true" in junit.stdout.splitlines(),
        "constructor_dependency_is_same_context_repo": "wiring same: true" in junit.stdout.splitlines(),
        "framework_owned_context_lifecycle": True,
        "business_behavior_tested": False
    }
}
(E / "java-verification-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(junit.stdout)
print("Actual Spring TestContext smoke test: 1 test passed; no business behavior test was executed.")
