# Reproducible production — Dependency resolution

Approved topic: Dependency resolution. Publication: 2026-11-24, proposed 19:00 Asia/Phnom_Penh. Internal curriculum identifiers belong only to directories/production records, not public media. Manual publication approval remains required.

## Java verification

`java/run.sh` uses pinned Spring/spring-test 6.2.11, JUnit 5.12.2/platform 1.12.2 and ECJ 3.40 targeting Java 17 on the captured JDK 21.0.13 runtime. Eleven dependency JARs have source/hash/license records. Three actual tests pass: compatible-type discovery/eligibility filtering/exact constructor reference; missing required type startup failure; and matching-but-ineligible-only startup failure. The two negative tests intentionally produce Spring context-initialization WARN output on stderr; this is not an empty-stderr claim.

SuccessConfig imports OrderService and registers eligibleGateway, backupGateway with autowireCandidate=false, and an unrelated AuditLogger deliberately named gateway. The parameter metadata says gateway, but that wrong-type bean cannot satisfy PaymentGateway. The observer-only TracingBeanFactory delegates all decisions to Spring and records the actual full candidate path exercised here. It finds two compatible names, excludes the backup from autowiring and supplies the same eligibleGateway reference to the constructor. The backup remains registered and retrievable by explicit lookup.

The negative contexts assert UnsatisfiedDependencyException with root NoSuchBeanDefinitionException and inactive context state. Genuine proof lines, JUnit reports, runtime trace and ten compiled/tested source hashes are retained under source/evidence/java-*. No standalone application/main invocation, real payment or comprehensive behavior test is claimed.

The exact Spring 6.2.11 implementation source is retained under java/framework/ with source provenance and licenses. Its dependency-name shortcut, qualified-name handling, eligible-candidate search and candidate-selection branches explain why this controlled match/filter/inject illustration must not be generalized into a universal type-first or name-only algorithm. Qualifiers, primary settings, names and other cases can affect selection.

## Voice and timing

Literal inputs are in script-input.json. `voice/setup.sh` creates a local environment and downloads pinned licensed Kokoro model/style files; `generate.py` performs coherent-scene male narration at normal 1.02 inference. `qa.py` retains unprompted local ASR and signal metrics; `split_captions.py` aligns display phrases to final speech. Any caption-only glossary/span mapping must retain the raw recognition and provenance. Never invent voice naturalness, pronunciation or perceived-age approval when auditory review is unavailable.

## Thumbnail, captions and animation

Unmodified Inter variable/OFL and DejaVu code-font assets are under assets/. The white heavy multiline thumbnail reads “How Spring / Finds Your / Dependencies”, highlighting only “Dependencies” in blue #0866FF. Runtime font axes, actual per-line sizes and geometry are recorded in thumbnail-style.json and font provenance. Source frame0 must equal cover.png before compression, including the separate full-hook caption “How does Spring know what to inject?” because the headline differs from the spoken phrase. The headline stays stable from 0–1s while the technical background moves; 1–2s transitions purposefully into explanation.

Captions use 52px Inter weight 700, actual textbbox glyph measurements, white text, a black at 82% RGBA rounded panel, padding 26/14, radius 12 and maximum 840px width in a dedicated region centered near 540/1380. Wrap coherent phrases instead of shrinking text. Renderer/preflight checks cover safe bounds; encoded QA inspects real opening 0/.5/1/2s, first-frame.png, cover similarity, transitions, captions, recap reading hold and separate Thanks.

`animation/audio_mix.py` creates the original NumPy bed/effects and records two-pass loudness normalization. `render.py` writes native 1080×1920/60 FPS frames and FFmpeg H.264/AAC 48kHz, Rec.709 SDR with fast-start metadata. `validate.py` checks the actual MP4 and current Java/voice evidence. `package_platforms.py` independently validates copied upload videos. `finalize_delivery.py` creates/checks lesson and ZIP manifests only after sources/reports freeze. The private mobile player is prepared locally; it is not deployed automatically.

## Rebuild

From the lesson directory:

```sh
bash source/rebuild.sh
```

Requires free/open-source Java runtime, Python 3/venv, curl, FFmpeg/FFprobe and network access for pinned dependencies. Speech models, environments and caches are setup inputs excluded from Git/packages. The script never pushes, uploads, schedules, deploys a live preview or publishes. Complete actual encoded review and QA/editorial records before finalizing archives. Follow platform-policy-review.md and current manual thumbnail/cover/disclosure controls before requesting publication approval.
