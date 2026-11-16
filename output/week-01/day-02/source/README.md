# Reproduce: ApplicationContext

This lesson uses an actual AnnotationConfigApplicationContext, original Pillow graphics, NumPy audio and locally inferred licensed Kokoro male narration. The approved topic remains ApplicationContext; the publication plan remains 2026-11-17, proposed 19:00 Asia/Phnom_Penh (12:00 UTC). These are planning fields only. No upload, scheduling or publication is performed.

## Actual Java example and tests

From the lesson directory:

```sh
bash source/java/run.sh
```

The application creates a new, unrefreshed AnnotationConfigApplicationContext, registers Config.class, calls refresh(), looks up Service, publishes a DemoEvent and closes the context. Infrastructure definitions are already present; the diagram illustrates the demo's application beans. Config has @Bean methods for Repo and Service(Repo). During refresh, Spring processes configuration into definitions before creating the demo's non-lazy singleton instances and supplying Repo to Service. A BeanFactoryPostProcessor observes the repo/service definitions before either corresponding singleton exists.

ApplicationContext delegates bean definition/instance handling to its bean factory and also provides higher-level container services. This demo exercises application-event delivery and managed singleton cleanup: Service implements ApplicationListener<DemoEvent> and DisposableBean. A successful lookup returns the already wired Service reference; repeated lookup returns that same default singleton, without repeating its construction. close() invokes its cleanup callback. The animated repo/service definitions are selected application beans, not an exhaustive list of Spring infrastructure definitions.

Two actual JUnit tests passed with no failures. The lifecycle test verifies configuration metadata before refresh, definition-before-instance ordering during refresh, actual Spring version, dependency identity, singleton reuse, service result, exactly one handled event and one cleanup callback even if close is called again. The second test verifies an @Lazy bean definition exists after refresh without an instance, and lookup then creates its shared singleton. The video therefore does not claim every definition is immediately instantiated or every bean scope has the same cleanup semantics.

Actual proof lines include:

```text
same service: true
events handled: 1
cleanup called: true
```

Main compilation, test compilation, JUnit and the standalone application all exited 0 with empty stderr. Exact commands, stdout, exit codes, JUnit XML, documentation evidence and source hashes are retained in evidence/java-*. See java/README.md for full reproduction and scope notes.

The verified toolchain is OpenJDK 21.0.13, Eclipse ECJ 3.40.0 compiling Java17-target classes, Spring Framework 6.2.11, Micrometer 1.15.4 and JUnit Jupiter 5.12.2 / console platform 1.12.2. The provided runner does not require Maven or javac. Ten pinned compiler/runtime/test jars have recorded download provenance, hashes and license notices. This is a Spring Framework example; Spring Boot is not used.

## Rebuild narration and video

Run source/rebuild.sh or these explicit steps from the lesson directory:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 0.90 --hook-speed 1.00 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
```

The production environment uses Python 3.12, Pillow 13.0.0, NumPy 2.3.5, SciPy 1.17.0 and FFmpeg/FFprobe 7.1.5. Voice dependencies have a separate locked environment. Kokoro model and voice bundle downloads are checksum-pinned in voice/models.sha256. Downloaded speech-model caches, environments and Python bytecode are excluded from Git and ZIP delivery.

Seven coherent scene-level utterances use the 80% am_puck / 20% am_fenrir male style blend. The hook uses model inference speed 1.00 and the other six phrases 0.90. Actual source narration is35.812000 s, rounded to35.816667 s at 60 FPS (2149 frames). The complete recap hold is32.275958–34.275958s before the separate Thanks scene. No waveform time stretching or pitch shifting is used. Source narration is ../narration.wav. Actual ASR, phonemes, pauses, pitch, signal measurements and listening-review limitations are in voice/. Those objective checks do not establish humanlike naturalness or perceived age. No auditory acceptance is claimed in this runtime.

## Immediate opening, recap and separate cover

The latest brief overrides the earlier static-cover opening: the actual MP4 begins with a visible technical mechanism and immediate spoken hook from frame one. The first scene progressively distinguishes definition recipes from actual managed objects. There is no title-card hold, fade-in, logo intro or black opening. cover.png is a separate 1080×1920 branded upload asset rather than an unchanged opening-second hold. Interfaces that select only a video frame can use a clear opening mechanism frame.

The seven scenes follow definition versus instance → configuration registration/refresh → created and wired singleton instances → getBean result → event dispatch/close-time cleanup → actual verification plus full mechanism overview → Thanks for watching. source/timing.json contains final sample-derived scene/hold times; ../storyboard.md describes the progressive visual cues. The complete recap holds for two seconds before the separate narrated Thanks card. Standalone recap.png and thanks.png supplement the same sequence embedded in the MP4.

Captions are burned into the picture from the opening hook, and subtitles.srt is exported separately. The recap fits above the reserved caption band. Important graphics remain inside X=90..990, Y=250..1520, with real decoded-frame/mobile-scale review recorded separately in ../verification-report.md.

animation/audio_mix.py synthesizes an original harmonic bed and subtle mechanism tones with NumPy, ducks music beneath speech and preserves continuity across scene cuts. No sampled song, stock effect or paid production service is used.

## Packages, review and finalization

Platform folders contain separate filenames, publishing copy, technical notes, FFprobe output and manifests. Parent delivery archives are day-02-youtube-shorts-upload.zip, day-02-facebook-reels-upload.zip and day-02-production.zip. The current ApplicationContext files replace the earlier Day 2 topic at the approved destination; that previous production is retained in Git history.

../asset-rights.md and ../originality-review.md document provenance, permissions and review limits. Font notices are in assets/; model/voice/inference license evidence is in voice/licenses/; Java dependency notices are in java/licenses/. No exhaustive plagiarism screening or global novelty claim is made.

After regeneration, inspect the actual encoded master and both platform copies, then update ../verification-report.md from current evidence. Run `python source/animation/finalize_delivery.py` after editorial and review files are final. It checks current platform manifests and ZIP members, creates the lesson SHA-256 manifest and complete production ZIP, verifies archived members, and writes parent archive hashes/delivery audit. The rebuild script does not push or publish. Repository AGENTS.md requires the production agent to push the generated files and sources after applicable checks, while disclosing every incomplete essential criterion.
