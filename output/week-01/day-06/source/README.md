# Reproduce: Multiple contexts

The exact approved topic is **Multiple contexts**, publication date **2026-11-21**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). These are prepared metadata only. This production does not upload, schedule or publish to YouTube or Facebook. Existing lessons are preserved.

## Actual Java behavior and verification

From the lesson directory:

```sh
bash source/java/run.sh
```

Independent `AnnotationConfigApplicationContext(AConfig.class)` and `AnnotationConfigApplicationContext(BConfig.class)` instances register demo beans alpha and beta respectively. Each can retrieve its own named bean. A cannot retrieve beta from B, and B cannot retrieve alpha from A. The missing lookups throw actual `NoSuchBeanDefinitionException` after successful initialization.

The hierarchy demonstration creates a **fresh** parent from ParentConfig and an initially empty child. The child calls `setParent(parent)`, registers ChildConfig, then calls `refresh()`. The child manages its local bean and can retrieve the parent's shared bean by name when that name is absent locally. `child.getBean("shared", Item.class)` returns the same object reference as the parent lookup. `child.containsLocalBean("shared")` is false: hierarchy lookup does not copy the parent bean into the child's registry. The parent's lookup of the child's local bean fails. The child closes before the parent, and closing the child leaves the parent active.

Actual verification is **four JUnit tests passed; zero failed**. Main/test compilation, JUnit and standalone ContextsDemo all exit successfully with empty stderr. Tests cover both-direction independent isolation; upward lookup plus local registry/listing boundaries and parent-instance identity; absence of reverse visibility; and a separate child's same-name local bean hiding the parent's named bean. The lesson demonstrates named lookup, without generalizing those rules to every listing/type-enumeration API.

Actual standalone proof includes:

```text
A alpha: alpha
B beta: beta
A beta: missing
A beta exception: NoSuchBeanDefinitionException
B alpha: missing
B alpha exception: NoSuchBeanDefinitionException
child shared: shared
child shared same: true
child owns shared: false
child local: local
parent local: missing
parent local exception: NoSuchBeanDefinitionException
parent active after child close: true
```

Exact commands, stdout, stderr, exit codes, JUnit XML, tested source hashes and five official Spring API documentation responses are retained under evidence/java-*. See java/README.md and java/technical-notes.md for the full reproduction. Actual tools are Spring Framework 6.2.11, OpenJDK 21.0.13, ECJ 3.40.0 targeting Java 17, Micrometer 1.15.4 and JUnit Jupiter 5.12.2 / console platform 1.12.2. Ten pinned jars have source URLs, verified hashes and retained licenses/notices. No Maven, javac or Spring Boot invocation is claimed.

## Rebuild narration, captions and video

Run source/rebuild.sh or the explicit steps:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model small.en
source/voice/.venv/bin/python source/voice/split_captions.py
python -m venv source/animation/.venv
source/animation/.venv/bin/pip install -r source/animation/requirements.txt
source/animation/.venv/bin/python source/animation/audio_mix.py
source/animation/.venv/bin/python source/animation/render.py --previews --render
source/animation/.venv/bin/python source/animation/validate.py
source/animation/.venv/bin/python source/animation/package_platforms.py
```

Rendering/audio dependencies are pinned separately from the locked voice dependencies. Model and voice downloads are checksum-pinned in voice/models.sha256. Downloaded models, environments, caches and Python bytecode are excluded from Git and ZIPs. Literal input text, pronunciation phonemes, coherent scene segments, raw unprompted ASR and signal/pause evidence remain in voice/.

The licensed 80% am_puck / 20% am_fenrir male English blend uses normal inference speed 1.02 for all seven scene batches, with 0.08-second ordinary joins. There is no waveform stretching or pitch shifting. The user rejected slowed 0.80 delivery on an earlier lesson; do not slow speech to fill the runtime target. Actual narration is 38.112500 seconds, with planned picture rounded up to 38.116667 seconds / 2287 frames at 60 FPS. The complete overview holds from 34.771750 to 36.771750 seconds, before the separate Thanks card. There are 22 SRT cues, maximum 34 characters. Final unprompted small.en recognition returns 91/91 words with two substitutions (“registry stays” versus intended “registries stay”), edit distance 2 and WER 2.1978%. The caption-only two-token mapping is documented separately without changing the raw ASR score. Exact final timing/captions are in timing.json, ../narration-script.md and ../storyboard.md; measured export metadata belongs in ../verification-report.md.

No auditory approval is claimed. Perceived younger-to-middle adult male age, human naturalness, subtle synthesis artifacts and final pronunciation acceptance remain unverified because no supported listening review is available. Licensed narration and objective checks do not complete that subjective acceptance requirement.

## Hook, registries and ending

The supplied hook is refined for pacing to “Two contexts. Different beans?” The complete source hook utterance is 1.705292 seconds. Separate registries and concrete lookup results are visible immediately, with purposeful motion from frame one. There is no static cover/title hold, greeting, fade or logo intro. cover.png is a separate 1080×1920 branded asset.

Seven scenes establish independent contexts and selected demo beans, show local and missing lookups, create a fresh parent-child pair in the correct initialization order, traverse the named lookup upward and return the existing parent reference, verify the reverse lookup failure and assemble the overview, then show Thanks. The completed overview holds for two seconds before that final card. recap.png and thanks.png supplement the same closing sequence inside the MP4.

Important content stays within X=90..990 and Y=250..1520; captions reserve their own band. The diagrams omit Spring infrastructure beans and show only the selected application beans. Animation timings illustrate cause and effect, not measured Spring lookup performance. Source snippets omit instrumentation; the complete runnable Java is retained.

The quiet music bed and effects are original Python/NumPy synthesis, with smooth envelopes and narration ducking. There is no sampled song, stock recording or paid production asset.

## Delivery and finalization

Platform folders contain separate video filenames, publishing text, technical notes, actual FFprobe output and SHA-256 manifests. Parent archives use day-06-youtube-shorts-upload.zip, day-06-facebook-reels-upload.zip and day-06-production.zip. The actual master and packaged copies require probe/decode/hash verification.

Asset provenance, commercially permitted font/model/dependency evidence and originality-review limits are in ../asset-rights.md and ../originality-review.md. Publishing copy links to the versioned BeanFactory and HierarchicalBeanFactory APIs. The two links are checked independently for publishing evidence. No exhaustive plagiarism check or worldwide novelty claim is made.

After reviewing the encoded video, root updates ../verification-report.md from actual evidence, then runs `python source/animation/finalize_delivery.py`. That step checks manifests and ZIP members, refreshes the lesson manifest and production archive, validates archived copies and records parent archive hashes/delivery audit. Do not change finalized inputs without refreshing the manifests and packages.

Phone delivery includes a deployed player with native controls, inline playback and a same-origin MP4 download button. Its reproducible source and deployment record are under mobile-preview/. A raw GitHub download URL alone does not supply the required preview player. Browser/on-phone checks must be reported according to what was actually performed.

The rebuild script does not push or publish. Repository AGENTS.md requires the production artifacts and sources to be pushed after applicable checks, while every incomplete requirement remains disclosed.
