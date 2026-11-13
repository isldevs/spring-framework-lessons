#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# No network download: use the pinned jars already retained with this lesson.
sha256sum -c dependencies.sha256 >/dev/null
mkdir -p ../evidence
config_build_dir=$(mktemp -d "${TMPDIR:-/tmp}/isldevs-config-flow.XXXXXX")
trap 'rm -rf "$config_build_dir"' EXIT
printf -v config_classpath '%s:' lib/*.jar
set +e
java -jar lib/ecj-3.40.0.jar -17 -parameters -cp "${config_classpath%:}" -d "$config_build_dir" ConfigFlowDemo.java >../evidence/config-java-compile.stdout.txt 2>../evidence/config-java-compile.stderr.txt
config_compile_status=$?
printf '%s\n' "$config_compile_status" >../evidence/config-java-compile.exit-code.txt
set -e
if ((config_compile_status != 0)); then
    cat ../evidence/config-java-compile.stderr.txt >&2
    exit "$config_compile_status"
fi
set +e
java -cp "$config_build_dir:lib/*" ConfigFlowDemo >../evidence/config-java-program.stdout.txt 2>../evidence/config-java-program.stderr.txt
config_run_status=$?
printf '%s\n' "$config_run_status" >../evidence/config-java-program.exit-code.txt
set -e
cat ../evidence/config-java-program.stdout.txt
if ((config_run_status != 0)); then
    cat ../evidence/config-java-program.stderr.txt >&2
fi
exit "$config_run_status"
