# Reproduce: Constructor Injection in Spring Boot

This lesson uses actual Spring Boot startup, a constructor-required PaymentGateway dependency, original Pillow graphics, NumPy audio and local licensed Kokoro male narration. Source speech is 35.819167 seconds, rounded up to 35.833333 seconds at 60 FPS. Final encoded stream measurements and remaining voice-acceptance limits are in ../verification-report.md.

## Actual Boot example and tests

CheckoutApplication has @SpringBootApplication in package lesson.orders and starts a real non-web SpringApplication. Its package scan discovers @Component DemoGateway and @Service OrderService. PaymentGateway is the interface; DemoGateway is the unique managed implementation in this example. OrderService's only constructor requires PaymentGateway, checks it with Objects.requireNonNull, and stores the supplied reference in a private final field. A final reference cannot be reassigned; it does not make the gateway object's state immutable.

The actual Boot integration test checks the runtime version, unique interface candidate, managed/injected reference identity, constructor-before-use ordering, simulated receipt and singleton reuse. A separate pure Java service test manually constructs OrderService with a RecordingGateway and verifies forwarded order ID, amount, call count and returned result. It does not add another production gateway bean.

```sh
bash source/java/run.sh
```

The runner downloads/checks pinned jars, compiles main and test sources separately, runs JUnit, then executes the standalone Boot application. Source and exact Java reproduction details are under java/. The verified toolchain is OpenJDK 21.0.13, ECJ 3.40.0 targeting Java 17, Spring Boot 3.5.6, Spring Framework 6.2.11, Micrometer 1.15.4, SnakeYAML 2.4 and JUnit Jupiter 5.12.2 / console platform 1.12.2. Maven and javac are not required by the provided runner.

Actual result: two JUnit tests succeeded, none failed; compilation, tests and standalone application exited 0 with empty stderr. Current stdout, commands, exit codes, JUnit XML, dependency/source hashes and official documentation evidence remain under evidence/java-*.

DemoGateway only returns an in-memory simulated approval such as APPROVED order-1042 USD 19.99. The recording fake is a separate test double. No real payment, card data or external payment API is involved.

## Rebuild narration and video

From the lesson directory, run source/rebuild.sh or the explicit steps:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 0.90 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
```

The production toolchain uses Python 3.12, Pillow 13.0.0, NumPy 2.3.5, SciPy 1.17.0 and FFmpeg/FFprobe 7.1.5. Voice dependencies have a separate locked environment. The Kokoro float32 model and voice bundle are locally inferred and checksum-pinned by voice/models.sha256; downloaded model caches and virtual environments are excluded from Git and the delivery ZIP.

This lesson uses 80% am_puck / 20% am_fenrir at actual inference speed 0.90, allowing calm phrasing while meeting the requested duration. This is model inference pacing, not waveform stretching or pitch shifting. Each of seven scenes is one coherent inference batch. Source narration is ../narration.wav; actual ASR, phonemes, pitch, pauses and review limits are in voice/. Those metrics do not constitute listening acceptance of human naturalness or intended age.

## Cover, recap and Thanks timing

The exact separate cover.png is the unchanged source for frames 0–59, without an overlay or fade; narration begins immediately. Encoded H.264 frames are compared against the supplied cover with normal lossy tolerance. This keeps the first video frame usable as a thumbnail for phone uploads.

The recap starts at 25.193375s. The completed-diagram reading hold runs **32.283125–34.283125s**, exactly 2 seconds. The requested Thanks card follows from **34.283125 to 35.819167s**, including the closing audio tail. The recap hold is not the last two seconds of the file.

The renderer keeps the interface contract, concrete DemoGateway object, constructor parameter, stored final reference, application use and separate fake test distinct. Its recap is a concrete Boot-startup/type-resolution/injection/use overview. The standalone recap.png and thanks.png supplement the sequence embedded in the same MP4. English captions are burned into the picture and subtitles.srt is supplied separately.

animation/audio_mix.py generates an original quiet harmonic bed and synchronized reference/verification cues with NumPy, ducks it beneath narration and preserves continuity across scene cuts. No sampled song or stock effect is used.

## Packages and review scope

Platform copies and their own manifests, FFprobe output, notes and paste-ready copy live in platforms/. Parent archives use day-03-youtube-shorts-upload.zip, day-03-facebook-reels-upload.zip and day-03-production.zip, preserving earlier lessons. Nothing is uploaded, scheduled or published to YouTube/Facebook.

../asset-rights.md and ../originality-review.md document actual asset provenance, licenses and review limits. Font notices are in assets/; model/voice and inference software evidence in voice/licenses/; runtime/compiler/test dependency notices in java/licenses/. Standard Java/Spring concepts are not claimed as globally novel; no exhaustive plagiarism search is claimed.

After regeneration, inspect the actual encoded master and both platform copies, then refresh verification-report.md. Run `python source/animation/finalize_delivery.py` after the report and editorial files are final. It checks both current platform manifests and ZIP members, creates the lesson SHA-256 manifest and complete production ZIP, verifies every archived member and writes the parent archive hashes/delivery audit. The local rebuild script does not push or publish; repository AGENTS.md requires the production agent to commit and push verified artifacts afterward. Any incomplete essential quality requirement must remain honestly disclosed.
