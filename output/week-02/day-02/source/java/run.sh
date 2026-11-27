#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f lib/spring-test-6.2.11.jar || ! -f dependencies.sha256 ]]; then
  python fetch-dependencies.py
fi
python verify.py
