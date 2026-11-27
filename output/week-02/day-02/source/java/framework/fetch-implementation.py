#!/usr/bin/env python3
"""Reproduce the pinned, official Spring source inspection evidence.

Uses Python's standard library. This downloads and verifies source artifacts;
it does not run the lesson's Java tests or generate a fabricated runtime trace.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen
import zipfile

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent.parent / "evidence"
VERSION = "6.2.11"
BASE = f"https://repo.maven.apache.org/maven2/org/springframework/spring-beans/{VERSION}/spring-beans-{VERSION}"
SOURCE_SHA256 = "f5fcf8046c9f5e0ef7cd183d2ac6b0e5d23cd7f27c174234243c71a5e6399c75"
BINARY_SHA256 = "f9ba5dedee94947b11d930209ff1a12bbe9e28b1b4f73c5baeba2fb3fe32d08e"
MEMBERS = [
    "org/springframework/beans/factory/support/DefaultListableBeanFactory.java",
    "org/springframework/beans/factory/annotation/AutowiredAnnotationBeanPostProcessor.java",
    "org/springframework/beans/factory/support/AutowireCandidateResolver.java",
    "org/springframework/beans/factory/support/SimpleAutowireCandidateResolver.java",
    "org/springframework/beans/factory/support/GenericTypeAwareAutowireCandidateResolver.java",
    "org/springframework/beans/factory/annotation/QualifierAnnotationAutowireCandidateResolver.java",
]


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def fetch(url: str) -> tuple[bytes, int]:
    with urlopen(url, timeout=30) as response:
        return response.read(), response.status


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    source_url = BASE + "-sources.jar"
    source, status = fetch(source_url)
    published_sha1, sha1_status = fetch(source_url + ".sha1")
    expected_sha1 = published_sha1.decode("ascii").strip()
    assert hashlib.sha1(source).hexdigest() == expected_sha1
    assert digest(source) == SOURCE_SHA256
    (HERE / f"spring-beans-{VERSION}-sources.jar").write_bytes(source)
    extracted = {}
    with zipfile.ZipFile(io.BytesIO(source)) as archive:
        license_members = [name for name in archive.namelist()
                           if "license" in name.lower() or "notice" in name.lower()]
        for member in MEMBERS:
            body = archive.read(member)
            name = Path(member).name
            (HERE / name).write_bytes(body)
            extracted[name] = digest(body)

    # Source JAR omits full LICENSE/NOTICE. Obtain both from the matching,
    # hash-pinned official binary without retaining another binary artifact.
    binary_url = BASE + ".jar"
    binary, binary_status = fetch(binary_url)
    assert digest(binary) == BINARY_SHA256
    license_provenance = {
        "binary_jar_url": binary_url,
        "http_status": binary_status,
        "binary_jar_sha256": digest(binary),
        "binary_jar_size_bytes": len(binary),
        "extracted_files": [],
    }
    with zipfile.ZipFile(io.BytesIO(binary)) as archive:
        for member, name in [("META-INF/license.txt", "LICENSE.txt"),
                             ("META-INF/notice.txt", "NOTICE.txt")]:
            body = archive.read(member)
            (HERE / name).write_bytes(body)
            license_provenance["extracted_files"].append({
                "file": name, "archive_member": member,
                "sha256": digest(body), "size_bytes": len(body),
            })
    save_json(HERE / "license-provenance.json", license_provenance)
    save_json(EVIDENCE / "java-implementation-sources.json", {
        "source_url": source_url, "http_status": status,
        "published_sha1_url": source_url + ".sha1",
        "published_sha1_http_status": sha1_status,
        "published_sha1_verified": expected_sha1,
        "size_bytes": len(source), "source_jar_sha256": digest(source),
        "version": VERSION, "extracted_files": extracted,
        "archive_license_members": license_members,
        "license_provenance_file": "../java/framework/license-provenance.json",
    })

    excerpts = [
        ("constructor-selection", "AutowiredAnnotationBeanPostProcessor.java", 450, 452,
         "The only declared constructor with parameters is a candidate without @Autowired."),
        ("resolve-entry", "DefaultListableBeanFactory.java", 1622, 1644,
         "Optional/provider/lazy cases are handled before ordinary resolution."),
        ("shortcut-and-value", "DefaultListableBeanFactory.java", 1648, 1663,
         "A pre-resolved shortcut and suggested value precede name and candidate search."),
        ("name-shortcut", "DefaultListableBeanFactory.java", 1682, 1707,
         "A dependency/suggested name shortcut must also satisfy type and eligibility checks."),
        ("full-search-and-required-failure", "DefaultListableBeanFactory.java", 1713, 1726,
         "An unresolved required singular dependency raises a missing-bean error."),
        ("single-candidate-selection", "DefaultListableBeanFactory.java", 1731, 1762,
         "Multiple matches need selection; one remaining match is used and validated."),
        ("type-discovery-and-eligibility", "DefaultListableBeanFactory.java", 1956, 1977,
         "Type-compatible bean names are discovered; self-reference and eligibility checks filter them."),
        ("fallback-candidate-passes", "DefaultListableBeanFactory.java", 1978, 2002,
         "Fallback and self-reference passes exist when the ordinary candidate pass is empty."),
        ("candidate-resolver-delegation", "DefaultListableBeanFactory.java", 956, 969,
         "The bean factory delegates eligibility to its configured candidate resolver."),
        ("candidate-definition-flag", "AutowireCandidateResolver.java", 44, 46,
         "The base eligibility check consults BeanDefinition.isAutowireCandidate()."),
        ("generic-type-eligibility", "GenericTypeAwareAutowireCandidateResolver.java", 64, 70,
         "Explicitly ineligible definitions fail before generic-type checks."),
        ("qualifier-eligibility", "QualifierAnnotationAutowireCandidateResolver.java", 156, 170,
         "The annotation-aware resolver preserves prior checks and considers qualifiers."),
        ("multiple-candidate-selection-policy", "DefaultListableBeanFactory.java", 2035, 2080,
         "Primary, dependency/suggested name, priority, default candidate and resolvable dependencies can affect selection."),
    ]
    records = []
    for key, file, start, end, claim in excerpts:
        lines = (HERE / file).read_text(encoding="utf-8").splitlines()
        records.append({
            "id": key, "file": "../java/framework/" + file,
            "source_file_sha256": extracted[file],
            "line_start": start, "line_end": end,
            "excerpt": "\n".join(lines[start - 1:end]), "interpretation": claim,
        })
    save_json(EVIDENCE / "java-implementation-inspection.json", {
        "evidence_kind": "official pinned source inspection, not runtime execution",
        "spring_version": VERSION, "source_jar_sha256": SOURCE_SHA256,
        "excerpts": records,
        "lesson_scope": "Simplified ordinary required PaymentGateway constructor dependency; not a complete universal resolution algorithm.",
    })
    md = ["# Spring 6.2.11 implementation excerpts", "",
          "These are verbatim excerpts from the hash-verified source JAR. They document implementation inspection, not test execution.", ""]
    for rec in records:
        md += ["## " + rec["id"], "", rec["file"] +
               f" (lines {rec['line_start']}–{rec['line_end']})", "",
               rec["interpretation"], "", "```java", rec["excerpt"], "```", ""]
    (EVIDENCE / "java-implementation-excerpts.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"version": VERSION, "source_http_status": status,
                      "source_sha256": SOURCE_SHA256,
                      "extracted_java_files": len(extracted),
                      "inspection_excerpts": len(records)}, indent=2))


if __name__ == "__main__":
    main()
