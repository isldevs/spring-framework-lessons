# Verification report — closing overview revision

**Video rendering, technical verification and two-platform packaging: COMPLETE. Strict perceptual voice acceptance: INCOMPLETE.** This runtime cannot ingest audio for a listening review, so perceived age, human naturalness and subtle synthesis artifacts remain unverified. No auditory acceptance is claimed. Nothing has been uploaded, scheduled or published to YouTube or Facebook.

Review date: 2026-11-13, Asia/Bangkok. Planned production date: 2026-11-16. These internal dates and schedule identifiers are not displayed publicly in the video or publishing copy.

## Approved change and persistent preference

The user approved a closing overview diagram and allowed up to 45 seconds when explanation needs more time. The final output remains strictly below 45 seconds. `AGENTS.md` now records that future lessons should finish with a progressively revealed mechanism recap, hold the complete diagram for at least two seconds, allow up to 45 seconds for clarity, and commit/push after each generation or revision.

The original cover and first five explanatory scene branches are unchanged; source-level comparison against the previous commit and cover SHA-256 are retained in `source/evidence/recap-change-summary.json`. Scene 6 replaces the former responsibility marker with the complete flow:

1. Register `@Bean` definitions.
2. Spring creates managed Repo and Service objects, then passes the Repo reference into Service.
3. The application sends a `getBean(Service.class)` request UP to the container.
4. The ready service reference returns DOWN to the application.
5. The qualification **Managed beans only** remains visible.

Creation/wiring visibly precedes the application request; getBean does not trigger a new-object animation. The container graph is already present when the lookup occurs. `recap.png` is a separate full-resolution image of the completed overview; the recap itself is embedded in the same MP4, not a separate clip.

## Actual encoded master

| Check | Actual result |
| --- | --- |
| Video/container duration | 44.383333s, below the authorized45s ceiling |
| Resolution and frame rate | Native 1080×1920, progressive, constant 60FPS |
| Codecs | H.264 High, AAC LC stereo 48kHz |
| Frames and timestamps | 2,663 decoded frames; every presentation timestamp checked at 1/60 s intervals |
| Pixel format / color | yuv420p 8-bit SDR, limited/TV range; BT.709 matrix, transfer and primaries |
| Audio duration | 44.368000s; video frame rounding adds approximately15ms of already quiet tail |
| Full decode | FFmpeg exit 0, empty error log |
| Encoded loudness | -16.08LUFS integrated, -1.31dBTP true peak, 4.00LU loudness range |
| Cover at start | Source frames0–59 are pixel-identical to cover.png before encoding, no fade-in; narration begins immediately |
| Encoded cover comparison | All60 decoded opening frames compared; mean SSIM 0.998971, minimum0.998913; ordinary lossy compression differences |
| Black frames | No black intervals detected |
| Final-mix continuity | No internal quiet interval at−50dBFS lasting≥0.15s; intended final quiet tail starts44.076292s |
| Subtitles | 23 synchronized cues; ordered, positive duration, nonoverlapping, within runtime; caption words match the scripted narration |
| Safe bounds | 178 source samples across scene/caption/opening states; bright foreground stays within X90..990/Y250..1520 |

Final MP4 SHA-256:

```text
bf2210acd945924d60504bb564904dae180e90ef73038106e4e4256d7e66f334
```

Raw FFprobe, full-decode, timestamp, loudness, silence, black-frame and opening-comparison results are retained under `source/evidence/final-*`. The current encoder explicitly writes H.264 VUI and MP4 Rec.709 tags; no post-render metadata repair was required.

## Completed-diagram reading hold

The reserved source reading hold runs **42.367792–44.367792s**, exactly 2.0seconds. The graph finishes earlier and remains stationary throughout that interval. The progress rail outside the diagram can continue moving.

The validator independently compared **120 source diagram crops pixel-for-pixel**, then compared **all 120 actual decoded hold frames** against the completed graph. The diagram crop is X100..980/Y534..1300, excluding captions and the progress rail. Source crops are identical; encoded SSIM minimum/mean is **0.998425/0.998425**, above the 0.995acceptance threshold. This verifies the actual delivered MP4, not merely an intended timeline.

Actual decoded frames were reviewed at mobile size: `source/evidence/final-decoded-mobile-contact.png` and `final-decoded-scene-6.png`. The request/return arrow directions are distinct, the Repo→Service reference is clear inside Spring, and the managed-bean qualification remains readable. No primary text clipping or crowding was observed. See `source/evidence/qa-notes.md` and `recap-qa-review.json` for the independent review.

## Narration, timing and review limits

Local Kokoro v1.0 float32ONNX uses the same80%am_puck/20%am_fenrir American-English male style blend at speed1.02. The styles are combined before inference to produce one consistent voice, not overlaid as two recordings. No pitch shifting, waveform time stretching, external speech service or substitute TTS was used. All six scenes fit one inference batch each. First-five-scene durations match the prior version.

Narration WAV is 44.367792s,48kHz mono PCM24, including the programmed2.0s final tail. Signal starts at 0.015250s; peak -1.514415dBFS, RMS -20.874903dBFS, zero clipped samples, zero endpoint samples. Four-millisecond quiet-edge microfades prevent edit clicks. Pitch10th/50th/90th percentiles are 86.34/112.61/168.73Hz, with 4.85semitones standard deviation. These metrics cannot certify perceived age or naturalness.

Independent Whisper base.en, without an initial prompt, returns 103 tokens for 102 expected words. Raw normalized WER is **1.9608%**: it splits “inversion” into “in version,” producing two edit-distance operations. The unmodified raw transcript and score are retained. The actual pronunciation input has the correct inversion phonemes. For caption alignment only, this one documented word-boundary split is merged; the audio and raw ASR score are not changed. This is NOT a claim of zero WER. See `source/voice/alignment-normalization.json`, `pronunciation-g2p.json`, `asr.json`, and `asr-summary.json`.

Caption and animation anchors use independent ASR word timestamps on an approximate20msgrid. Exact synthesis edit boundaries remain in `source/timing.json`. Recap anchors include Define30.620s, creation32.120s, wiring33.160s, request35.140s, ready36.560s, and the managed-bean qualifier38.580s. The quiet reference-return tone is synchronized to the return-arrow arrival at37.260s. The complete graph remains visible during the final 2 s reading hold while the original background bed fades naturally.

**Outstanding voice requirement:** no auditory listening review could be performed. The runtime does not support audio input. Humanlike smoothness, intended age impression and subtle speech artifacts must still be accepted or rejected by listening; automated ASR and pitch metrics do not substitute for that requirement. Details remain in `source/voice/voice-qa.md`.

## Scene timings

| Scene | Actual source timeline |
| --- | --- |
| 1 | 0.000000–1.891083 s |
| 2 | 1.891083–7.146625 s |
| 3 | 7.146625–15.349708 s |
| 4 | 15.349708–20.163375 s |
| 5 | 20.163375–29.250625 s |
| 6 | 29.250625–44.367792 s |

## Java/Spring verification retained

The Java example and pinned dependencies are unchanged. It was actually compiled with ECJ3.40.0 and executed with OpenJDK21.0.13/Spring6.2.11. Successful exit 0 with empty stderr; actual preserved stdout:

```text
manual wiring: true
spring wiring: true
same singleton: true
unmanaged same as bean: false
```

`@Bean Service service(Repo repo)` receives the repository bean from Spring and passes it to `new Service(repo)`. The application requests Service through `ctx.getBean(Service.class)`, and the assertion verifies its repository is the same instance returned by `ctx.getBean(Repo.class)`. Repeated service lookup returns the same default singleton; an independent `new Repo()` is distinct. These non-lazy singleton beans are created at context refresh, before lookup. The on-screen `spring wiring: true` is an excerpt of that actual run.

Reproduce with `bash source/java/run.sh`. Official Spring documentation snapshots/excerpts remain under `source/evidence/java-*`, including IoC introduction, @Bean factory parameters and default singleton scope:

- https://docs.spring.io/spring-framework/reference/core/beans/introduction.html
- https://docs.spring.io/spring-framework/reference/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html

## Rights, packages and reproduction

`asset-rights.md` and `originality-review.md` document actual provenance and limitations. The cover, recap, animation, narration text, NumPy music and sound effects were created for this production. Licensed OpenSans/DejaVu fonts, Apache-2.0 Kokoro male styles and open-source tools are retained with their license evidence. No paid stock footage, proprietary font, sampled song, named-person voice imitation, or exhaustive-plagiarism-search claim is involved.

Both platform MP4s were independently probed and fully decoded with exit 0/empty error logs. Their SHA-256 equals the master, and both covers/SRT copies equal their source files. `source/evidence/platform-validation-summary.json` and platform-specific command logs contain current values. Each self-contained upload ZIP includes the video, cover, synchronized SRT, paste-ready platform copy, upload notes, technical/voice review notes and checksums. YouTube also includes search tags and pinned comment text. No YouTube/Facebook publication or scheduling occurred.

Run `source/rebuild.sh` for generation, validation and platform packaging. `checksums.sha256` covers the requested deliverables and current source/evidence, excluding itself, virtual environments, model caches and Python bytecode. Downloaded model/voice hashes have their own verified manifest. The complete production ZIP contains the current lesson, recap PNG, both platform folders, scripts, evidence and licenses. Run `sha256sum -c checksums.sha256` inside the lesson directory; the two platform ZIPs have a separate `platform-archives.sha256`. Normal Git commits retain previous delivered versions, and `AGENTS.md` persists the user's future-generation preferences.
