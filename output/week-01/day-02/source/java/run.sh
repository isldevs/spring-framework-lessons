#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# The retained binary dependencies are pinned. Download only when absent.
if ! sha256sum -c dependencies.sha256 >/dev/null 2>&1; then
    python3 fetch-dependencies.py
    sha256sum -c dependencies.sha256 >/dev/null
fi
mkdir -p build
printf -v spring_classpath '%s:' lib/*.jar
java -jar lib/ecj-3.40.0.jar -17 -parameters -warn:none -cp "${spring_classpath%:}" -d build src/lesson/di/*.java
java -cp 'build:lib/*' lesson.di.DiDemo
