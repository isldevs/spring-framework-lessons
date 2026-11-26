# Reproducible production — Constructor injection

Approved curriculum: Constructor injection, publication2026-11-23, proposed19:00Asia/Phnom_Penh. Internal scheduling identifiers belong only to directories/production records, not public media. Manual publication approval remains required.

## Java verification

`java/run.sh` uses pinned Spring/spring-test6.2.11, JUnit5.12.2/platform1.12.2 and ECJ3.40 targetingJava17 on the captured JDK21 runtime. Eleven dependency JARs have source/hash/license records. Two actual tests passed: managed implicit single-constructor wiring/execution, and a manual-new caller-supplied dependency control. No constructor@Autowired exists on OrderService; exactly one PaymentGateway candidate is registered by Config's imports. `gateway()` exposes the reference for this small verification example; `placeOrder(2500)` delegates to the in-memory demo gateway and returns `demo-paid:2500`.

Genuine JUnit proof lines are retained in source/evidence/java-junit.stdout.txt and java-verification-result.json. Five source hashes match the compiled/tested code. There is no standalone application/main invocation or real payment claim. This is a selected context and deterministic demo execution, not comprehensive business validation.

## Voice and timing

Literal inputs are in script-input.json. `voice/setup.sh` creates a local environment and downloads the pinned licensed Kokoro model/styles; `generate.py` performs local male narration at normal1.02 inference. `qa.py` retains unprompted local ASR and signal metrics; `split_captions.py` aligns display phrases to the final speech. Any caption-only normalization must retain raw recognition/provenance. No voice naturalness, pronunciation or perceived-age approval may be invented when auditory review is unavailable.

## Thumbnail, captions and animation

Unmodified Inter variable/OFL and DejaVu code-font assets are under assets/. The heavy white multiline thumbnail uses Inter weight900 at104/96/104px and blue#0866FF rounded keyword highlighting. Captions use Inter weight700 at52px; stylesJSON and font-axis provenance are authoritative. source frame0 must equal cover.png before compression, including the separate full-hook caption because the headline is not the literal spoken phrase. Stable headline0–1s, meaningful background motion and a purposeful1–2s transition replace the older no-cover opening convention.

Bold52px Inter captions use actual textbbox measurements, white glyphs, black82% RGBA rounded panels, padding26/14, max width840 and a dedicated region centered near540/1380. Font axes, geometry and actual values are recorded by thumbnail-style.json/subtitle-style.json. Renderer/preflight code checks safe bounds; final encoded checks must inspect actual opening0/.5/1/2s, first-frame.png, cover similarity, motion, transitions, captions and recap/Thanks.

`animation/audio_mix.py` generates the original NumPy bed/effects and measures two-pass loudness normalization. `render.py` writes native1080×1920/60FPS frames and FFmpeg H.264/AAC48kHz, Rec.709SDR with fast-start metadata. `validate.py` checks the real MP4, current Java/voice evidence and encoded frames. `package_platforms.py` independently validates each copied upload video. `finalize_delivery.py` creates/checks lesson and ZIP manifests only after all sources/reports are frozen.

## Rebuild

From the lesson directory:

```sh
bash source/rebuild.sh
```

Requires free/open-source Java runtime, Python3/venv, curl, FFmpeg/FFprobe and network access for pinned dependencies. Speech models/environments/caches are setup inputs and are not committed or packaged. The script never pushes, uploads, schedules or publishes. Finish actual encoded review and final QA/editorial records before finalizing archives. Follow platform-policy-review.md and the account's current manual thumbnail/cover/disclosure controls before requesting publication approval.
