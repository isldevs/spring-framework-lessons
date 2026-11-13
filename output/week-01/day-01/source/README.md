# Reproduce this iSLDevs short

The MP4 is fully rendered. Strict completion is **INCOMPLETE** because this runtime cannot ingest audio for perceptual naturalness review. See `../verification-report.md` and `voice/voice-qa.md`. Do not treat an objective speech transcript check as a listening review. Nothing has been published to YouTube or Facebook.

## Toolchain

- Python 3.12; Pillow 13.0.0; NumPy 2.3.5; SciPy 1.17.0.
- FFmpeg/FFprobe 7.1.5, libx264 and native AAC; 1080×1920 at 60 fps.
- Local Kokoro v1.0 float32 ONNX, an 80% `am_puck` / 20% `am_fenrir` American English male blend, speed 1.02; pinned inference dependencies in `voice/requirements-lock.txt`.
- OpenJDK 21.0.13, Eclipse ECJ 3.40.0, Spring Framework 6.2.11.

## Run from the deliverable directory

```sh
# Real Java/Spring behavior and assertions; dependencies have pinned hashes.
bash source/java/run.sh
# Trace Config construction, factory calls, wiring and later singleton lookup.
bash source/java/run-config-flow.sh

# Locally generate speech (downloads licensed model/voice bundle).
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --voice am_puck80_fenrir20
# Independent ASR and prosody QA, then split long captions using word timestamps.
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py

# Create an isolated renderer environment if needed.
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews
source/animation/.venv/bin/python source/animation/render.py --render
```

`render.py` writes `cover.png`, `subtitles.srt`, and `video.mp4`. The cover's source pixels are used unchanged for every frame in 0–1s; MP4 decoding has normal lossy encoding differences. The narration starts at zero; the measured signal onset is recorded in `voice/voice-qa.md`. Longer captions are aligned with independent ASR word timestamps; full-scene synthesis boundaries are exact. Scene transitions follow the actual speech duration in `timing.json`. No hard-coded fake Java terminal output was generated: the displayed proof line is copied from the successful actual run in `evidence/java-program.stdout.txt`.

The additional [Config-to-bean execution trace](java/config-flow-notes.md) shows the application supplying `Config.class`, Spring instantiating the configuration and invoking `repo()` and `service(repo)`, then later `getBean` returning the ready singleton without another factory call. It uses the same pinned Java/Spring dependencies; compiler/runtime results are retained separately.

## Audio and animation

The approved cover and first five explanatory scenes are retained. The closing recap now makes Config explicit: the application starts Spring with `Config.class`; Spring reads the configuration and invokes its `@Bean` factory methods; Repo is created and supplied to Service; the application retrieves the ready service with `getBean`. Config is the Java class whose annotated factory methods provide the creation recipes. The completed diagram is held for two seconds, followed by the brief “Thanks for watching” end card.

The user permits up to 45 seconds when the explanation needs it; clarity takes priority over forcing the video into 35–40 seconds. Seven whole-scene utterances maintain connected phrasing without mid-sentence edit splices. The requested younger-to-middle adult male style uses the same inference-time blend, with no pitch shifting. Perceived age and human-like naturalness remain listening-acceptance criteria, not facts established by voice names or automated metrics.

The current source timeline is **43.403417 seconds**, rounded up to **43.416667 seconds** at 60 FPS. The recap is scene 6, starting at 29.250625 seconds. Its speech ends and the completed-diagram reading hold begins at **39.962667 seconds**; `recap_hold_end` is **41.962667 seconds** and `recap_hold_seconds` is **2.0**. The Thanks card is scene 7, from **41.962667 to 43.403417 seconds**, including the final 350 ms audio tail. The recap hold is before the Thanks card, not the final two seconds of the file. `recap_cues` and `recap_cues_absolute` align the diagram to actual speech timestamps. The first five scene boundaries are unchanged.

`animation/audio_mix.py` creates original harmonic background audio and brief reference-transfer tones with NumPy, ducks the music beneath speech, and applies measured two-pass EBU R128 normalization. `animation/sound-events.json` records each visual cue time. The narrator is retained separately as `../narration.wav`. `animation/render.py` is the full original Pillow motion source, including all seven scenes and burned-in caption layout. Previews also export `../recap.png` and `../thanks.png`. `timing.json` includes the exact script as `phrases`, display cues as `captions`, scene boundaries, the explicit recap reading hold and the Thanks-card interval.

## Rights and source evidence

All rendered graphics, diagrams, script, background music, and sound effects are original for this production. Open Sans is Apache-2.0; DejaVu Sans Mono has the bundled permissive font license (`assets/*LICENSE.txt`). Kokoro model/voice rights, inference-code MIT license, official model card, and male-voice table are retained in `voice/licenses/`. Java/Spring dependency licenses and notices are in `java/licenses/`. Spring is Apache-2.0. Official documentation snapshots and extracted claims are in `evidence/java-*`. Software used for synthesis, graphics, verification and encoding is free/open-source. No stock clips, proprietary fonts, or paid assets are used.

Rerunning synthesis on a different hardware/runtime version may have minor floating-point differences; the checked-in WAV, timing, dependency locks, downloaded model hashes, and source preserve this actual render. Recompute checksums only after all outputs and reports are final.

## Platform delivery packages

The approved master is copied losslessly to `platforms/youtube-shorts/youtube-shorts.mp4` and `platforms/facebook-reels/facebook-reels.mp4`. Each folder includes the exact cover, synchronized SRT, paste-ready platform copy, upload notes, FFprobe output, technical/voice review notes, and its own checksum manifest. Export packaging is complete; perceptual voice approval remains unverified. Nothing has been uploaded or published to YouTube or Facebook.

Recreate the export packages after validating the master:

```sh
source/animation/.venv/bin/python source/animation/package_platforms.py
```

The script checks codec, dimensions, frame rate, color tags, duration and byte identity, then verifies file checksums and ZIP integrity. Independent full decodes for each delivered platform file are retained under `source/evidence/platform-*`. The two ZIP archives are written to the parent output directory as `youtube-shorts-upload.zip` and `facebook-reels-upload.zip`.
