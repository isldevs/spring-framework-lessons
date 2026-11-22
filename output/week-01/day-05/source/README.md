# Reproduce: Bean naming

The exact approved topic is **Bean naming**, publication date **2026-11-20**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). These are prepared metadata only. Nothing is uploaded, scheduled or published by this production. Prior lessons are preserved.

## Actual Java behavior and verification

From the lesson directory:

```sh
bash source/java/run.sh
```

AlphaConfig declares `@Bean("alpha") Client client()`. The explicit bean name is alpha while the Java factory method remains client. The first context contains one Client: `getBean("alpha")`, `getBean("alpha", Client.class)` and `getBean(Client.class)` all return the same default singleton.

A **fresh separate context** registers AlphaConfig and BetaConfig. The latter declares `@Bean("beta") Client backup()`. Alpha and beta are different instances of the same Client type. Both named lookups still select their bean; the typed-name overload also checks that selected bean's type. With no primary or other preference in this example, direct `getBean(Client.class)` throws NoUniqueBeanDefinitionException with two candidates. Other selection policies such as @Primary can change type-lookup outcomes; the lesson does not claim every multi-candidate context must fail.

Actual verification is **4 JUnit tests passed; 0 failed**. Main/test compilation, JUnit and standalone NamingDemo exit0 with empty stderr. Tests verify the explicit-name/factory-method distinction and single-instance identity; two named instances with ambiguous type query; a selected-name type guard using BeanNotOfRequiredTypeException; and a separate constructor `@Qualifier("beta")` case. That qualifier can select beta for injection while direct type-only lookup remains ambiguous. Bean names can participate in qualifier matching, but named lookup and qualifier injection are not the same API.

Actual standalone proof includes:

```text
named alpha: alpha
typed name alpha: alpha
single type same: true
named beta: beta
type lookup: NoUniqueBeanDefinitionException
type candidates: 2
```

Exact commands/stdout/stderr/exit codes, JUnit XML, source hashes and seven official-documentation responses are retained in evidence/java-*. See java/README.md and java/technical-notes.md for complete reproduction. The actual toolchain is Spring Framework6.2.11, OpenJDK21.0.13, ECJ3.40.0 compiling Java17-target classes, Micrometer1.15.4 and JUnit Jupiter5.12.2 / console platform1.12.2. Ten pinned jars have download provenance, verified hashes and license/notices. No Maven, javac or Spring Boot invocation is claimed.

## Rebuild audio and video

Run source/rebuild.sh or the explicit steps:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
```

Rendering/audio dependencies are pinned in animation/requirements.txt, with separate locked voice dependencies. Model and voice downloads are checksum-pinned in voice/models.sha256. Downloaded models, environments, caches and Python bytecode are excluded from Git and ZIPs. Voice input text, phonemes, coherent per-scene segments, raw unprompted ASR and signal/pause measurements remain in voice/.

The licensed80%am_puck/20%am_fenrir male English blend uses normal conversational inference at1.02, with brief0.08s scene joins. No waveform stretching or pitch shifting is used. Do not slow speech merely to fill a duration target: the user rejected an earlier0.80 edition of another lesson. Actual narration lasts39.286167s, with picture rounded to39.300000s/2358frames at60FPS. There are23captions, maximum35characters. The complete recap reading hold is35.945417–37.945417s before Thanks. Actual script/utterance details are in ../narration-script.md, ../storyboard.md and timing.json. Fresh unprompted ASR measures97expected/97recognized words with0edit distance and0WER; raw evidence is preserved.

No auditory approval is claimed. Perceived younger-to-middle adult male age, human naturalness, subtle synthesis artifacts and final pronunciation acceptance remain unverified because the runtime cannot ingest audio for listening review. Actual licensed narration is delivered, but those objective checks do not complete subjective acceptance.

## Hook, diagrams and ending

The original hook is refined for technical accuracy and spoken pacing to “Two names. One ambiguous type.” The example's distinct names do not by themselves choose a type candidate. A concrete named-bean map and type-query ambiguity are visible immediately; there is no static title/cover hold, greeting, fade or logo intro. cover.png is a separate1080×1920 branded asset.

Seven scenes show explicit alpha registration; named and typed-name lookup; single-Client type identity; a fresh two-Client context; type ambiguity without primary selection; actual proof plus overview; and Thanks. The completed overview is held for two seconds before the separate spoken Thanks card. recap.png and thanks.png supplement the same sequence embedded in the MP4. Important content stays within X=90..990,Y=250..1520; captions reserve their own band.

The picture distinguishes name identity from Java type, preserves the managed object while a reference returns to the app, and labels the fresh context for the second example. Animation times explain causality, not Spring performance. Source snippets omit instrumentation; runnable full Java is included.

Music and effects are original Python/NumPy synthesis with smooth envelopes and speech ducking. No sampled song, stock recording or paid production service is used.

## Delivery and finalization

Platform folders contain separate filenames, publishing text, technical notes, FFprobe output and manifests. Parent archives are day-05-youtube-shorts-upload.zip, day-05-facebook-reels-upload.zip and day-05-production.zip. The master and packaged copies must be verified using actual probe/decode/hash results rather than assumed from source settings.

Asset provenance, commercially compatible font/model/dependency license evidence and originality-review limits are in ../asset-rights.md and ../originality-review.md. Both final public Spring reference URLs were separately fetched with HTTP200; response hashes/resolved URLs remain in evidence/publishing-reference-check.json. No exhaustive plagiarism check or worldwide novelty claim is made.

After final encoded review, update ../verification-report.md from actual results and run `python source/animation/finalize_delivery.py`. It verifies platform manifests/ZIP members, refreshes the lesson manifest and production ZIP, checks every archived member and writes parent archive hashes/delivery audit. Source/rebuild.sh does not push or publish; repository AGENTS.md requires production artifacts to be pushed after applicable checks while every incomplete requirement remains disclosed.
