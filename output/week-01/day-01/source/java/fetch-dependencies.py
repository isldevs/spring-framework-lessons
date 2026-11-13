#!/usr/bin/env python3
"""Download pinned Apache/EPL libraries from Maven Central, verify published SHA-1.
Keep generated SHA-256 manifest for artifact provenance. TLS verification is enabled.
"""
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "lib"
LIB.mkdir(exist_ok=True)
COORDINATES = [
    ("org.springframework", "spring-context", "6.2.11"),
    ("org.springframework", "spring-aop", "6.2.11"),
    ("org.springframework", "spring-beans", "6.2.11"),
    ("org.springframework", "spring-core", "6.2.11"),
    ("org.springframework", "spring-expression", "6.2.11"),
    ("org.springframework", "spring-jcl", "6.2.11"),
    ("io.micrometer", "micrometer-observation", "1.14.11"),
    ("io.micrometer", "micrometer-commons", "1.14.11"),
    ("org.eclipse.jdt", "ecj", "3.40.0"),
]
manifest = []
for group, artifact, version in COORDINATES:
    name = f"{artifact}-{version}.jar"
    url = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/{name}"
    path = LIB / name
    data = path.read_bytes() if path.exists() else urllib.request.urlopen(url, timeout=60).read()
    expected = urllib.request.urlopen(url + ".sha1", timeout=30).read().decode().strip().split()[0]
    if hashlib.sha1(data).hexdigest() != expected:
        raise RuntimeError(f"Checksum mismatch for {name}")
    path.write_bytes(data)
    manifest.append(f"{hashlib.sha256(data).hexdigest()}  lib/{name}")
    print(name, len(data), "published SHA-1 verified")
(ROOT / "dependencies.sha256").write_text("\n".join(manifest) + "\n")
