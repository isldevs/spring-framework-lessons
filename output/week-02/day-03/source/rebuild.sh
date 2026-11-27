#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash source/java/run.sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py
source/voice/.venv/bin/python source/voice/qa.py --asr-model small.en
source/voice/.venv/bin/python source/voice/align.py
python3 source/animation/audio_mix.py
python3 source/animation/render.py --render
python3 source/animation/validate.py
# Inspect actual encoded evidence, update reports, then run deliver.py.
# Never claim listening acceptance or publish automatically.
