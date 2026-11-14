# Reproduce: How Spring Dependency Injection Works

This production uses a real component-scanning/constructor-injection example, original Pillow graphics and NumPy audio, plus local licensed Kokoro male narration. The source speech timeline is 35.649833 s, including the two-second recap hold and the closing Thanks card; the 60 FPS MP4 rounds up to 35.650000 s. Actual final stream measurements and all remaining acceptance limits belong in ../verification-report.md.

## Technical example

Config enables @ComponentScan("lesson.di"). Spring discovers @Repository Repo and @Service OrderService, registers their definitions, resolves the single OrderService(Repo repo) constructor's Repo parameter by type, and supplies the repository reference. The example has one Repo candidate. A single constructor requires no @Autowired annotation. Default non-lazy singleton startup builds the graph before the application requests and uses the service; that timing is not a claim about every scope or lazy bean.

The actual Java program verifies the injected reference is the same repository bean returned by the context and that the application uses a ready, wired service. Real output, constructor/startup ordering and official documentation evidence are retained under evidence/java-*. The runnable sources are in java/src/lesson/di/.

```sh
bash source/java/run.sh
```

Pinned environment: OpenJDK 21.0.13 runtime, Eclipse ECJ 3.40.0 compiler targeting Java 17, Spring Framework 6.2.11 and Micrometer 1.14.11. Dependency download URLs, SHA-256 and licenses are retained under java/. No Spring Boot, web server or handwritten service locator is involved.

## Rebuild the narration and video

From the lesson directory, use source/rebuild.sh or these explicit steps:

```sh
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
```

The toolchain is Python 3.12, Pillow 13.0.0, NumPy 2.3.5, SciPy 1.17.0 and FFmpeg/FFprobe 7.1.5. Voice dependencies are pinned separately in voice/requirements-lock.txt. The local Kokoro v1.0 float32 model and voice bundle are checksum-pinned in voice/models.sha256; model caches and virtual environments are recreated rather than placed in the delivery ZIP or Git.

Voice style is 80%am_puck / 20%am_fenrir, targeting a younger-to-middle adult male explanatory delivery, at speed 1.02. All seven scenes use coherent utterances. Source narration is retained as ../narration.wav. See voice/README.md, voice/voice-qa.md and raw ASR/phoneme/prosody metrics for the actual generation and review scope. These checks do not constitute auditory acceptance. Naturalness and perceived age remain unverified when this runtime cannot ingest audio for listening.

## Timing and drawings

The exact cover is rendered as the source image for frames 0–59, without an overlay or fade; narration begins immediately. The source cover is also delivered separately as ../cover.png for custom-cover workflows. Lossy H.264 decoding naturally differs slightly from PNG pixels; the actual encoded opening is compared by the validator.

Scene boundaries and caption cues come from actual synthesis and independent ASR word timestamps in timing.json. The last explanation scene starts 25.153958 s. Its speech finishes 32.209083 s; the completed diagram remains visible from 32.209083 to 34.209083 s. The final Thanks card follows, from 34.209083 to 35.649833 s. Do not test the last two seconds of the whole movie as if they were the recap hold.

animation/render.py contains the complete original motion graphics. Discovery metadata, matching constructor type, runtime object creation, reference injection and application use are kept distinct. animation/audio_mix.py creates the original quiet harmonic score and soft synchronized reference tones; no sampled music or stock effect is used. The renderer exports ../recap.png and ../thanks.png as supplementary images where implemented. English captions are burned into the MP4; ../subtitles.srt remains available as a separate accessibility track.

## Delivery and rights

Platform folders contain lossless master copies, the exact cover, synchronized SRT, technical checks and paste-ready copy. The archives are ../day-02-youtube-shorts-upload.zip and ../day-02-facebook-reels-upload.zip; the full archive is ../day-02-production.zip. Unique filenames preserve the previous lesson's packages. Nothing is uploaded, scheduled or published to YouTube/Facebook.

../asset-rights.md and ../originality-review.md document actual asset provenance and review limits. Font notices and complete licenses remain in assets/; Kokoro licensing and male voice evidence in voice/licenses/; Java dependency/compiler notices in java/licenses/. Technical concepts and standard Java/Spring idioms are not claimed as globally novel. No exhaustive plagiarism service or auditory approval is claimed.

After any regeneration, inspect the actual encoded output and both platform copies, then refresh verification-report.md, checksums.sha256, the platform/archive manifests and ZIPs. The delivered manifests describe one actual render, not hypothetical output. This rebuild script deliberately does not mutate a Git branch or publish a platform video; the repository AGENTS.md instructs the production agent to commit and push verified artifacts after each generation.
