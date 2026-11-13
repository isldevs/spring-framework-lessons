# Verification report — revised male voice

**Platform packaging: COMPLETE. Technical checks: PASSED. Strict perceptual voice acceptance: INCOMPLETE.** The revised MP4 and all requested deliverables exist and pass technical checks. Local Kokoro now targets a younger-to-middle adult male explanatory delivery. This environment cannot ingest audio for a listening review, so perceived age, smooth human naturalness and absence of subtle voice artifacts remain unverified. No auditory approval is claimed. Nothing has been published.

Production schedule: 2026-11-16. Checks performed 2026-11-13 UTC.

## Requested revision

The approved animation and cover have been retained. Their source/file SHA-256 values match `source/evidence/approved-animation-baseline.json`, as does the Java example. The animation was retimed to the revised narration, with newly aligned captions and sound events.

Voice style is **80% Kokoro am_puck + 20% am_fenrir**, both officially listed American English male styles with target quality B. Style embeddings are blended before inference to create one consistent voice; two audio tracks are not overlaid. There is no pitch shifting, time stretching, replacement TTS or imitation of a named person. Perceived age is a delivery target, not a verified speaker age.

For connected explanatory phrasing, six whole-scene utterances replace eleven separately synthesized clause snippets. Each scene is asserted to fit exactly one inference batch, with no mid-scene edit splice. Script words are unchanged; takeaway punctuation was adjusted for sentence breathing. Speed is 1.02. Added scene gaps are 200–260 ms, plus a 450 ms programmed final tail. Model-generated decays contribute additional quiet time. Edit endpoints use 4 ms microfades.

## Actual final video

| Check | Result |
| --- | --- |
| Codec / container | MP4, H.264 High profile, AAC LC |
| Resolution / rate | 1080 × 1920, progressive, constant 60 FPS |
| Decoded frames / timestamps | 2,215 frames; every presentation timestamp checked at 1/60 s intervals |
| Duration | Video/container 36.916667 s; AAC 36.915000 s; within 35–40 s and strictly under 45 s |
| Color | 8-bit yuv420p SDR, limited/TV range; BT.709 matrix, transfer and primaries |
| Audio | AAC, 48 kHz stereo; separate clean narration is 48 kHz mono PCM24 |
| Full decode | FFmpeg exit 0; empty decode error log |
| Encoded audio measurements | -16.18 LUFS integrated; -1.36 dBTP; 4.40 LU loudness range |
| Exact opening cover | Frames 0–59 use the supplied cover pixels unchanged before encoding; no fade-in |
| Encoded opening fidelity | First 60 decoded frames compared with cover; mean SSIM 0.998971, minimum 0.998913; normal lossy differences |
| Black intervals | None detected over the full encoded video |
| Captions | 18 SRT cues; ordered, positive duration, non-overlapping and within runtime; words match narration |
| Safe-area samples | 173 samples across scene/caption/opening states; bright foreground within X=90..990 and Y=250..1520 |

The revised encoder writes H.264 VUI color metadata explicitly through `h264_metadata` as well as MP4 tags. This current render required no subsequent metadata repair. The original baseline's missing-tag observation is retained separately as `source/evidence/baseline-initial-color-check.json`.

Final MP4 SHA-256:

```text
ea61b553d14b9be050b9cfccb2d092435196a2b75845ff7cd9d328f81f5d7a76
```

Raw commands, FFprobe output, full decode results, encoded loudness/silence scans, opening SSIM, frame timestamps and decoded PNGs are in `source/evidence/final-*`. See `source/evidence/qa-notes.md` for independent final-file findings.

## Narration and pronunciation checks

Actual narration duration is 36.915542 s, 48,000 Hz, mono, 24-bit PCM. First signal above −60 dBFS occurs at 0.015250 s, with no artificial initial silence. Peak -1.514415 dBFS; RMS -20.686998 dBFS; zero clipped samples; both endpoint samples zero.

Independent Whisper **base.en**, int8, beam size 5, no initial prompt, recognizes all 88 words with normalized word error rate 0.0. This includes Java, repository, bean definitions, get bean, inversion of control and managed beans. The smaller tiny.en diagnostic had confused five singular instances of bean with being; the larger independent check resolved those. No transcript prompt or manual correction was used to force a passing ASR result. Actual G2P phonemes are retained: bean `/bˈiːn/`, being `/bˈiːɪŋ/`, get bean `/ɡɛt bˈiːn/`.

Voiced pitch 10th/50th/90th percentiles are 87.34/112.61/173.67 Hz, with 4.71 semitones standard deviation across 2,292 voiced frames. This demonstrates varied pitch, not naturalness or age. Narration silence scan at −45 dBFS finds a longest internal quiet span of 0.837562 s at the verification-to-takeaway transition, including sentence decay and the designed scene gap; longest within-scene sentence pause is approximately 0.326 s. Final source quiet span is 0.868542 s, including decay and tail. The complete ASR transcript supports that no words disappeared.

Caption scene edit boundaries are exact sample-derived synthesis boundaries. The 18 short display cues use independent base.en word timestamps, approximate on a 20 ms grid. Maximum caption length is 45 characters. Spoken “get bean” is displayed as `getBean`. All scenes were rendered with synchronized original music, quiet reference-transfer tones and burned captions; separate SRT is supplied.

**Outstanding requirement:** a competent listening review of the actual final mix must accept or reject smoothness, age impression, pronunciation and any synthesis artifacts. Numeric pitch/ASR metrics cannot replace that review. The runtime explicitly returned “audio content omitted because you do not support audio input” in the original listening attempt; no listening capability has become available. See `source/voice/voice-qa.md` for the full limitation.

## Visual review and timing

Both source previews and actual decoded final-video frames were inspected at mobile size. Headlines, code, object labels and captions are readable, with no visible clipping or overlap of primary content. Code is approximately 39–40 px, captions 43 px, and headlines 62–102 px at 1080-wide delivery. Auxiliary node labels are smaller and supplemental. Background grid/glow extends beyond the safe area; important content does not. The first second has no caption overlay so the exact cover remains visible; its displayed question supplies the hook and the separate SRT starts at zero.

| Scene | Actual time |
| --- | --- |
| 1 | 0.000000–1.891083 s |
| 2 | 1.891083–7.146625 s |
| 3 | 7.146625–15.349708 s |
| 4 | 15.349708–20.163375 s |
| 5 | 20.163375–29.250625 s |
| 6 | 29.250625–36.915542 s |

The same six meaningful animation actions remain: an opening reference highlight, manual wiring, definitions producing a runtime graph, a resolved repository reference reaching the service constructor, an application request and returned ready service reference, and responsibility moving to Spring. No public week/day/lesson/episode numbering is shown.

## Verified Java/Spring behavior

The unchanged reproducible example was actually compiled with Eclipse ECJ 3.40.0 and executed with OpenJDK 21.0.13 and Spring Framework 6.2.11. The successful run exited 0 with empty stderr. Actual retained stdout:

```text
manual wiring: true
spring wiring: true
same singleton: true
unmanaged same as bean: false
```

Manual application code creates Repo then Service(repo). In the Spring configuration, `@Bean Service service(Repo repo)` has its factory parameter resolved by Spring, and returns `new Service(repo)`. The application calls `ctx.getBean(Service.class)` for its dependency. The assertion verifies that the service holds the same repository returned by `ctx.getBean(Repo.class)` and that service lookups return the same default singleton. An independent `new Repo()` is a distinct unmanaged object.

These non-lazy default singletons are created during context refresh; the lookup animation retrieves the ready service. It does not show a new object on every lookup or a service internally calling getBean. Spring manages registered beans rather than every Java object. The displayed `spring wiring: true` proof is an excerpt of the actual successful output, not fabricated terminal footage.

Official documentation snapshots and excerpts remain under `source/evidence/java-*`:

- https://docs.spring.io/spring-framework/reference/core/beans/introduction.html
- https://docs.spring.io/spring-framework/reference/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html

Run `bash source/java/run.sh`. Dependency versions, hashes, sources, build commands and licenses are retained under `source/java/`.

## Rights and reproduction

All graphics, diagrams, narration text, NumPy background music and sound effects are original. Software is free/open-source; no paid assets, stock clips, proprietary fonts or sampled music are used. Open Sans and DejaVu license texts are retained in `source/assets/`. Kokoro model/voice distribution is Apache-2.0; inference software is MIT. Official model card, male voice table, release details and license evidence remain in `source/voice/licenses/`. Both used voice styles are part of that distribution, with no separate noncommercial restriction identified. Java/Spring/compiler notices remain in `source/java/licenses/`.

Rebuild with `source/rebuild.sh` or the commands in `source/README.md`. The exact style blend, punctuation, pacing and one-batch-per-scene checks are in `source/voice/generate.py`; model files are local and pinned by `source/voice/models.sha256`. The original production archive has been preserved outside this revision as `../day-01-original-production.zip`.

All ten requested deliverables are present. `checksums.sha256` covers the nine other requested deliverables and retained source/evidence files outside virtual environments, model caches and Python bytecode. Model downloads have their own verified manifest. Run `sha256sum -c checksums.sha256` from this directory. The updated optional production ZIP includes deliverables, source and evidence, excluding recreatable virtual environments and model caches. No publication or upload has been performed.

## Two-platform delivery

Separate YouTube Shorts and Facebook Reels packages have been created without changing the approved master. Each actual platform file was independently probed, SHA-256 compared, and fully decoded with exit 0 and empty error output. Both videos are byte-identical to the master (SHA-256 shown above), so this introduces no generation loss. Both exact cover copies are 1080 × 1920, and both SRT copies contain the same 18 valid cues. Raw per-export results are retained in `source/evidence/platform-*`.

- `platforms/youtube-shorts/`: `youtube-shorts.mp4`, `cover.png`, `subtitles.srt`, title, description with hashtags, pinned comment, upload notes, FFprobe JSON, technical/voice review notes and checksum manifest.
- `platforms/facebook-reels/`: `facebook-reels.mp4`, `cover.png`, `subtitles.srt`, caption with hashtags, upload notes, FFprobe JSON, technical/voice review notes and checksum manifest.

The self-contained ZIPs are `../youtube-shorts-upload.zip` and `../facebook-reels-upload.zip`. Public copy contains no internal week/day/lesson numbering. Cover selection instructions account for interfaces that only permit choosing an existing frame; the exact cover is visible in the opening second. Captions are already burned in, and the optional SRT is retained for accessible caption tracks rather than a second decorative overlay.

Export preparation and technical validation are complete. The perceptual voice limitation described above remains disclosed inside each package. No upload, account access, scheduling or publication occurred.

## Delivery index and supplementary reviews

The final handoff includes separate `asset-rights.md` and `originality-review.md` records, plus comma-separated YouTube tags in `youtube-metadata.md` and `platforms/youtube-shorts/tags.txt`. These additions document actual asset provenance and review scope; they do not claim an exhaustive plagiarism search or a perceptual voice approval. The source/package checksum manifests have been refreshed after adding these documents.
