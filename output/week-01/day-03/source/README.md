# Reproduce: Bean registration

The approved topic is **Bean registration**, with the original publication date **2026-11-18** and proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). These are metadata fields only. Nothing is uploaded, scheduled or published by this production.

## Actual Java examples and tests

From the lesson directory:

```sh
bash source/java/run.sh
```

The application uses separate AnnotationConfigApplicationContext instances for the missing class, explicit factory configuration and component scan. A plain Client class on the classpath has no registration in the first refreshed context, so getBean(Client.class) throws the expected NoSuchBeanDefinitionException. The demonstration catches that expected missing-bean result rather than crashing or fabricating an error log.

For the factory path, ctx.register(FactoryConfig.class) activates @Configuration with an @Bean Client client() method. During refresh, Spring registers its factory-method definition before invoking the method and managing the returned Client. A BeanFactoryPostProcessor observes the definition, factory bean/method metadata and lack of a Client singleton before creation.

For the scanning path, the application registers ScanConfig, whose @ComponentScan("lesson.scan") discovers @Component Worker. Its class-based definition exists before the Worker singleton. The annotated Outside class lives in lesson.outside and remains excluded from that configured scan. An annotation alone does not activate scanning, and the package boundary matters. The pictures illustrate selected application definitions, not an exhaustive list of Spring infrastructure beans.

Actual verification: **3 JUnit tests passed; 0 failed**. They check the unregistered lookup, factory definition and single factory call, both retrievable default singletons, repeated-lookup identity, scanned class metadata and outside-package exclusion. Main compilation, test compilation, JUnit and the standalone application all exited 0 with empty stderr. Actual proof includes:

```text
plain class missing: true
@Bean retrieved: true
scan retrieved: true
outside scan missing: true
```

Exact commands, stdout, exit codes, source/dependency hashes, JUnit XML and official documentation evidence are under evidence/java-*. See java/README.md for full reproduction and scope. The actual toolchain is OpenJDK 21.0.13, Eclipse ECJ 3.40.0 compiling Java17-target classes, Spring Framework 6.2.11, Micrometer 1.15.4 and JUnit Jupiter 5.12.2 / console platform 1.12.2. Ten pinned jars have download provenance, hashes and notices. The provided runner does not require Maven or javac. Spring Boot is not used.

Both illustrated paths create bean definitions before their corresponding instances. This is not a universal claim that every Spring registration API requires a BeanDefinition: direct singleton registration and other APIs are outside this focused lesson. Creation and reuse shown here are default non-lazy singleton behavior, not a promise for every scope or lazy arrangement.

## Rebuild narration and video

Run source/rebuild.sh, or the explicit steps from the lesson directory:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 0.80 --hook-speed 1.00 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
```

The production environment uses Python 3.12, Pillow 13.0.0, NumPy 2.3.5, SciPy 1.17.0 and FFmpeg/FFprobe 7.1.5. Voice dependencies have a separate locked environment. Kokoro model and voice bundle downloads are checksum-pinned in voice/models.sha256. Downloaded models, caches, environments and Python bytecode are excluded from Git and ZIP delivery.

Seven coherent utterances use the licensed 80% am_puck / 20% am_fenrir male English blend. Only the short hook uses inference speed 1.00; the other phrases use 0.80. These are model inference controls, not waveform stretching or pitch shifting. Actual sample-derived utterance times, scene cuts, caption cues and the exact two-second recap hold are retained in timing.json and ../storyboard.md. Actual source narration is38.387208s, frame-rounded to38.400000s/2304frames. The complete recap hold is34.679125–36.679125s before Thanks. Source narration is ../narration.wav. Raw full-stream ASR is72expected/73recognized words, edit distance2, WER2.7778%; the classpath/class path spacing discrepancy is preserved in raw results and separately normalized for alignment. Phonemes, signal/pitch/pause measurements and alignment provenance are in voice/.

No auditory acceptance is claimed. Humanlike naturalness, perceived younger-to-middle adult male age, subtle synthesis artifacts and final pronunciation require listening that is unavailable in this runtime. Objective recognition and signal metrics do not satisfy that essential review, so strict overall approval remains incomplete.

## Immediate hook, separate cover and recap

The video starts from frame one with a visible plain-class/missing-registration mechanism and spoken hook. It has no title-card hold, fade-in, logo intro or black opening. cover.png is a separate 1080×1920 branded asset. If an upload interface selects a video frame rather than a separate cover, choose a clear opening mechanism frame.

Seven scenes follow missing class → missing definition/cause → registered @Bean factory configuration → configured component scan → outside-package annotation still missing → genuine proof and two-path overview → Thanks for watching. The overview is complete for at least two seconds before the separate narrated Thanks card. recap.png and thanks.png supplement the same ending embedded in the video.

Captions are burned into the picture from the opening hook and exported as synchronized subtitles.srt. The recap fits above its reserved caption band. Important content remains inside X=90..990, Y=250..1520; the encoded-file report separately records actual safe-bound, mobile-scale, transition and closing inspections. Animation timestamps explain the mechanism rather than benchmark Spring's execution speed.

animation/audio_mix.py synthesizes a quiet original harmonic bed and timed registration effects with NumPy. Speech ducking and smooth envelopes preserve continuity. No sampled song, stock recording or paid production service is used.

## Packages, rights and finalization

Platform folders have separate filenames, paste-ready copy, technical notes, FFprobe output and manifests. Parent archives use day-03-youtube-shorts-upload.zip, day-03-facebook-reels-upload.zip and day-03-production.zip. Current Bean registration media replace the earlier different-topic production at this approved destination; earlier versions remain in Git history.

../asset-rights.md and ../originality-review.md record provenance, permissions and review limitations. Font notices are in assets/, model/voice/inference evidence in voice/licenses/, and compiler/runtime/test notices in java/licenses/. Both public Spring reference URLs were actually retrieved with HTTP200; response hashes and resolved URLs are in evidence/publishing-reference-check.json. No exhaustive plagiarism check or worldwide novelty claim is made.

After regeneration, inspect the actual encoded master and both platform copies, then update ../verification-report.md from current results. Run `python source/animation/finalize_delivery.py` after all editorial and review files are final. It checks platform manifests and ZIP members, refreshes the lesson SHA-256 manifest and complete production ZIP, verifies archived members and writes parent archive hashes/delivery audit. The rebuild script does not push or publish. Repository AGENTS.md requires the production agent to push artifacts after applicable checks while disclosing every incomplete requirement.
