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
    "--select-class", "lesson.resolution.DependencyResolutionTest", "--reports-dir",
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
assert found == 3 and failed == 0 and skipped == 0, reports
proofs = ["compatible candidates: 2", "eligible candidates: 1", "unrelated ignored: true", "gateway same: true", "missing candidate: true", "missing exception: NoSuchBeanDefinitionException", "missing startup exception: UnsatisfiedDependencyException", "disabled candidate missing: true", "disabled compatible candidates: 1", "disabled eligible candidates: 0"]
assert all(line in junit.stdout.splitlines() for line in proofs)
hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / "src").rglob("*.java"))}
(E / "java-source-hashes.sha256").write_text("".join(v+"  "+k+"\n" for k,v in hashes.items()))
trace = [line.removeprefix("TRACE ") for line in junit.stdout.splitlines() if line.startswith("TRACE ")]
assert any(line == "eligible candidates: [eligibleGateway]" for line in trace), trace
(E / "java-runtime-trace.json").write_text(json.dumps({"observer":"TracingBeanFactory subclass delegates all decisions to Spring", "spring_framework_version":"6.2.11", "events":trace, "scope":"Actual successful PaymentGateway constructor dependency; not a universal resolution sequence or timing benchmark."},indent=2)+"\n")
result = {
 "spring_framework_version":"6.2.11", "spring_test_version":"6.2.11", "junit_jupiter_version":"5.12.2", "junit_platform_version":"1.12.2", "micrometer_version":"1.15.4", "compiler":"ECJ3.40.0", "class_file_target":"Java17", "runtime":version.stderr.strip(),
 "compile_main_exit_code":main.returncode,"compile_tests_exit_code":tests.returncode,"junit_exit_code":junit.returncode,"compile_stderr_empty":not main.stderr and not tests.stderr,"junit_stderr_empty":not junit.stderr,"expected_negative_context_warnings":True,
 "application_execution":"Not performed; actual JUnit tests create and close Spring contexts.", "junit_reports":reports,"tests_found":found,"tests_succeeded":found-failed-skipped,"tests_failed":failed,"tests_skipped":skipped,"proof_lines":[line for line in junit.stdout.splitlines() if line in proofs],"test_stdout_proof_lines":proofs,"source_sha256":hashes,"runtime_trace_file":"java-runtime-trace.json",
 "context_loading_mechanism":"JUnit methods use AnnotationConfigApplicationContext with an observer-only TracingBeanFactory and explicit Config registration/refresh/close.",
 "scope":"Three actual JUnit tests cover compatible type discovery, eligible-candidate filtering, unrelated same-named bean exclusion, exact constructor injection and missing/disabled candidate startup failures. No standalone app, payment, universal type-first resolution order or performance claim.",
 "verified_semantics":{"compatible_type_candidates_discovered":True,"unrelated_named_bean_ignored_for_required_type":True,"autowire_disabled_candidate_filtered":True,"one_eligible_gateway_injected_by_reference":True,"missing_required_candidate_fails_startup":True,"matching_disabled_bean_is_not_eligible":True,"real_payment_performed":False}
}
(E / "java-verification-result.json").write_text(json.dumps(result,indent=2)+"\n")
print(junit.stdout)
print("Actual dependency-resolution verification: 3 tests passed; expected negative-context warnings captured.")
