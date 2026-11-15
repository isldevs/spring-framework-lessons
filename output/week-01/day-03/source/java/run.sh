#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 fetch-dependencies.py
python3 verify.py
