#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v java >/dev/null
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
bash source/java/run.sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
# Inspect actual QA and refresh the final reports, manifests and production ZIP.
# Listening acceptance remains separate; never invent a perceptual approval.
# No Git push or social-platform publication is performed by this local rebuild.
