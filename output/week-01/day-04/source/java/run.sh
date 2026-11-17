#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
# Shared pinned dependencies already retained in this repository.
classpath=$(python -c 'from pathlib import Path; print(":".join(str(p.resolve()) for p in sorted(Path("../../../day-03/source/java/lib").glob("*.jar"))))')
java -jar ../../../day-03/source/java/lib/ecj-3.40.0.jar -17 -cp "$classpath" -d build MissingBeanDemo.java
java -cp "build:$classpath" MissingBeanDemo
