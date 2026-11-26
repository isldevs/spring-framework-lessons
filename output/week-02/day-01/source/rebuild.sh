#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v java >/dev/null
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
bash source/java/run.sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model small.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --preflight --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
# Inspect actual encoded evidence and complete all final reports, then run:
# python source/animation/finalize_delivery.py
# Never invent auditory acceptance. Publication requires manual approval.
# This script never pushes, uploads, schedules or publishes.
