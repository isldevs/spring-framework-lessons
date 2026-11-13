#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 fetch-dependencies.py
mkdir -p build
# ECJ is an open-source compiler; only a Java runtime is needed on this machine.
printf -v spring_classpath '%s:' lib/*.jar
java -jar lib/ecj-3.40.0.jar -17 -parameters -cp "${spring_classpath%:}" -d build IoCDemo.java
java -cp 'build:lib/*' IoCDemo
