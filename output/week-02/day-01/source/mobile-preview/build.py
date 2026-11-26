#!/usr/bin/env python3
"""Build the phone player from this lesson's final, unchanged media."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
LESSON = HERE.parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", type=Path)
parser.add_argument("--project-id", help="Exact registered Site ID; omit for an unpublished local preview")
args = parser.parse_args()
video = LESSON / "video.mp4"
probe = json.loads(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(video)
]))
duration = float(probe["format"]["duration"])
if args.project_id:
    manifest = args.output / ".openai/hosting.json"
    data = json.loads(manifest.read_text()) if manifest.exists() else {}
    if data.get("project_id", args.project_id) != args.project_id:
        raise SystemExit("Refusing to replace a different Site's identity.")
    data.update({"project_id": args.project_id, "static": {"directory": "dist"}})
    manifest.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(manifest)
args.output.mkdir(parents=True, exist_ok=True)
dist = args.output / "dist"
dist.mkdir(exist_ok=True)
html = (HERE / "index.html").read_text().replace("{{DURATION}}", f"{duration:.2f}")
(dist / "index.html").write_text(html)
for name in ("video.mp4", "cover.png", "subtitles.srt"):
    shutil.copy2(LESSON / name, dist / name)
master_hash = hashlib.sha256(video.read_bytes()).hexdigest()
assert hashlib.sha256((dist / "video.mp4").read_bytes()).hexdigest() == master_hash
print(json.dumps({"output": str(args.output), "duration_seconds": duration, "video_sha256": master_hash}))
