# Reproduce: Context smoke test

The exact approved topic is **Context smoke test**, publication date **2026-11-22**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The approved date remains unchanged even when production finishes later. This production prepares metadata and files without uploading, scheduling or publishing to YouTube or Facebook.

## Actual JUnit/Spring verification

From the lesson directory:

```sh
bash source/java/run.sh
```

`@SpringJUnitConfig(Config.class)` enables Spring's JUnit Jupiter integration and declares the selected test configuration. Spring loads that configuration and makes the test context available through an `@Autowired ApplicationContext` field. JUnit owns the test fixture; the illustration does not treat the fixture as a managed application bean. No specific ApplicationContext implementation is asserted.

Config declares `@Bean Repo repo()` and `@Bean OrderService service(Repo repo)`. Spring supplies the repository bean to the factory method and the OrderService constructor. The default singleton demo graph is ready before the test performs its lookup; those later lookups do not rerun the factories in this example.

The single actual test, `ContextSmokeTest.contextLoadsAndWires`, retrieves OrderService and Repo by type, checks that both are non-null and uses `assertSame(repo, service.repository())` to verify the expected reference identity. It also checks the Spring version used by this reproducible example. Object identity is the dependency assertion; equal values alone would not establish that relationship. This expectation is appropriate to the default singleton demo graph. Prototype or other scopes can require different assertions; assertSame is not a universal rule for every dependency.

Actual main/test compilation and JUnit execution exited 0 with empty stderr. **One JUnit test passed, zero failed or skipped.** No standalone application execution is claimed. Successful test stdout is emitted only after the real assertions pass:

```text
bean found: true
wiring same: true
```

The test covers the selected Config, required bean retrieval and expected constructor dependency. It does not prove order behavior, database operations, other configuration, all lazy beans or every application feature. Those need appropriate separate tests. The example uses `@DirtiesContext(AFTER_CLASS)` for deliberate demo cleanup; Spring's test context can otherwise be cached for compatible test configurations. This is not a claim that every test method gets a fresh context or that every application needs this cleanup annotation.

Actual tools: Spring Framework and spring-test 6.2.11, OpenJDK 21.0.13, ECJ 3.40 targeting Java 17, Micrometer 1.15.4, JUnit Jupiter 5.12.2 / Platform 1.12.2. Eleven pinned jars have source URLs, verified hashes and license/notices. No Maven, javac or Spring Boot execution is claimed. Complete commands, stdout/stderr, exit codes, JUnit XML, tested source hashes and six official Spring/JUnit documentation responses are retained under evidence/java-*. See java/README.md and java/technical-notes.md.

## Rebuild narration, captions and video

Run source/rebuild.sh or these explicit steps:

```sh
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
```

Rendering/audio dependencies are pinned separately from locked voice dependencies. Model/style downloads are checksum-pinned in voice/models.sha256. Downloaded models, environments, caches and Python bytecode are excluded from Git and ZIPs. Literal final narration, pronunciation phonemes, coherent scene segments, raw unprompted ASR and signal/pause evidence remain under voice/.

Use normal inference 1.02 for the licensed 80% am_puck / 20% am_fenrir male English blend. Ordinary joins are 0.08s; do not slow narration merely to fill a duration target. No waveform stretching or pitch shifting is used. Actual final narration is 36.985542s, with planned picture ceiling 37.000000s / 2220 frames. The complete recap holds 33.644792–35.644792s before separate Thanks. There are 20 SRT cues, maximum 34 characters. Final raw unprompted small.en recognition records 78 expected / 78 observed words, 6 edits and WER 7.6923%; no zero-error recognition claim is made. Four caption-only transformations are documented: two bean/being labels, the they/are contraction merge and a shared observed lookup span for look/up. No unobserved within-word boundary is claimed; raw transcript and score remain unchanged. Exact final timing/captions are documented in timing.json, ../narration-script.md and ../storyboard.md; actual encoded metadata belongs in ../verification-report.md.

Automated ASR, pronunciation phonemes, signal/pitch and pause measurements are objective evidence, not a listening review. No auditory approval is claimed for smooth human delivery, perceived younger-to-middle adult age, subtle synthesis artifacts or final pronunciation acceptance unless an actual listening review is available and performed. Disclose that remaining requirement in the final handoff.

## Opening, mechanism and ending

The supplied hook is shortened for pacing and scope to “Context loaded. Wiring checked?” A ready-context signal and a pending expected-reference check are visible immediately, with purposeful animation from frame one. Context readiness is not depicted as comprehensive business correctness. The branded 1080×1920 cover is separate; there is no static cover hold, greeting, fade or logo intro.

Seven scenes follow the Spring/JUnit configuration load and constructor wiring; required service lookup; repository reference identity assertion; actual passing smoke-test evidence; a progressive mechanism recap and business-testing boundary; then separate Thanks. The complete overview holds for at least two seconds **before** the Thanks card. Only selected application beans are drawn; Spring infrastructure beans and the JUnit-owned test fixture are not represented as extra managed application objects.

Important text, diagrams and captions stay inside X=90..990 / Y=250..1520. Captions reserve a separate lower band. Animation timings illustrate cause and effect and are not measurements of Spring or JUnit runtime performance. Source snippets omit instrumentation; complete compilable Java remains available.

The quiet background bed and effects are original Python/NumPy synthesis with smooth envelopes, narration ducking and meaningful event cues. No sampled song, stock recording or paid production asset is used.

## Delivery and finalization

Platform folders contain separate video filenames, publishing text, technical notes, actual FFprobe output and SHA-256 manifests. Parent archives use day-07-youtube-shorts-upload.zip, day-07-facebook-reels-upload.zip and day-07-production.zip. Actual master and packaged copies require probe/decode/hash verification.

Asset provenance and commercially permitted font/model/dependency evidence are recorded in ../asset-rights.md. ../originality-review.md states provenance and assessment limits rather than global novelty or exhaustive plagiarism claims. Publishing copy links to the versioned SpringJUnitConfig and SpringExtension API pages; those exact references are checked independently for delivery evidence.

After reviewing actual encoded media, root updates ../verification-report.md and runs `python source/animation/finalize_delivery.py`. This verifies manifests/ZIP members, refreshes the lesson manifest and production archive, and records archive hashes/delivery audit. Refresh manifests and packages after any finalized input changes.

Phone delivery includes a deployed player with native controls, inline playback and a same-origin MP4 download button. Its source and deployment record are under mobile-preview/. A raw GitHub URL alone does not meet the preview/player requirement. Browser/on-phone checks must be reported according to what was actually performed.

The rebuild script does not push or publish. Repository AGENTS.md governs final Git delivery and the required complete handoff, including direct web downloads and five separate phone-copyable publishing text blocks. Every incomplete requirement remains disclosed.
