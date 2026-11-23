#!/usr/bin/env python3
"""Rebuild the owner-private Bean naming player from verified lesson assets."""
import argparse
import hashlib
import json
import pathlib
import shutil

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROJECT_ID = "appgprj_6b047779cd208191a67df679c22738a2"
VIDEO_SHA256 = "3b882122e03afd42b9505b6e7f570741719c3704f86ca11b1453ee92584c9c83"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", type=pathlib.Path)
args = parser.parse_args()
lesson = REPO / "output/week-01/day-05"
video = lesson / "video.mp4"
if hashlib.sha256(video.read_bytes()).hexdigest() != VIDEO_SHA256:
    raise SystemExit("Master changed: review the new media before rebuilding the player.")
manifest = args.output / ".openai/hosting.json"
if manifest.exists():
    data = json.loads(manifest.read_text())
    if data.get("project_id") != PROJECT_ID:
        raise SystemExit("Refusing to overwrite a different Site's manifest.")
else:
    data = {"project_id": PROJECT_ID}
data["static"] = {"directory": "dist"}
manifest.parent.mkdir(parents=True, exist_ok=True)
manifest.write_text(json.dumps(data, indent=2) + "\n")
dist = args.output / "dist"
dist.mkdir(exist_ok=True)
shutil.copy2(HERE / "index.html", dist / "index.html")
for name in ("video.mp4", "cover.png"):
    shutil.copy2(lesson / name, dist / name)
print(f"Prepared mobile player in {args.output}; video hash verified.")
