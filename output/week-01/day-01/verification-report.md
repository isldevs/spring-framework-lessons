# Verification report — explicit Config flow and Thanks ending

**Rendering and technical QA: COMPLETE. Platform packaging: COMPLETE after the recorded per-export checks. Perceptual voice acceptance: INCOMPLETE.** This runtime cannot ingest audio for a listening review, so perceived age, human naturalness and subtle voice artifacts remain unverified. No auditory approval is claimed. Nothing has been uploaded, scheduled or published to YouTube or Facebook.

Review date:2026-11-13 (Asia/Bangkok). Planned production date:2026-11-16. Internal tracking labels are not displayed in the video or public publishing copy.

## User-requested change

The generic definitions overview has been replaced with the actual causal Config sequence. The cover and first five explanatory scene branches are unchanged. A seventh scene says and displays **Thanks for watching** after the completed recap has been held for two seconds. The total remains strictly below the authorized45-second ceiling. `AGENTS.md` records these future production preferences and the standing push-after-generation instruction.

The recap now shows:

1. Application code starts `AnnotationConfigApplicationContext` with `Config.class`, assigning it to `ctx`.
2. Spring reads `@Configuration class Config`, which declares actual `@Bean Repo repo()` and `@Bean Service service(Repo repo)` factory signatures.
3. Spring calls the factories, creates Repo, and passes the repository reference to Service. The corresponding rows and objects are revealed sequentially.
4. The application later calls `ctx.getBean(Service.class)` on that same context and receives the ready Service reference.
5. **Managed beans only** remains visible; no new object creation is animated during lookup.

The overview badge spells out **Inversion of Control** to name the mechanism being explained. `recap.png` shows the completed diagram. `thanks.png` shows the end card. Both sequences are inside the same final MP4, and the opening still uses the exact original cover from0–1s.

## Actual encoded file

| Check | Actual result |
| --- | --- |
| Container/video duration | 43.416667s, strictly below 45s |
| Display / frame rate | Native 1080×1920, progressive, constant 60FPS |
| Codecs | H.264 High; AAC LC stereo 48kHz |
| Frames/timestamps | 2,605 decoded frames; all timestamp intervals verified at1/60s |
| Color | yuv420p 8-bit SDR; BT.709 matrix, transfer and primaries; limited/TV range |
| Audio duration | 43.403000s; ordinary final video-frame rounding |
| Full decoding | Exit 0, empty error log |
| Loudness / peak | -15.94 LUFS, -1.38 dBTP, 4.40 LU loudness range |
| Opening cover | All 60 source frames pixel-identical; decoded meanSSIM0.998971/min0.998913 |
| Black intervals | None detected |
| Continuity | No unexpected internal silence at−50dBFS/150ms; intended final quiet tail begins43.228646s |
| Captions | 21 positive-duration, ordered, nonoverlapping SRT cues within runtime; exact script-word match |
| Safe bounds | 192 samples pass X90..990/Y250..1520 |

Final MP4 SHA-256:

```text
03eeaca3cb3fcfd445587ba1ef6e35b8e06e5ba7a4d15873fd1194c822a144ff
```

## Recap hold and actual last-frame checks

The completed mechanism is held for exactly **2.0s**, **39.962667–41.962667s**, inside scene 6. This is before the Thanks card, not at the file's endpoint.

All 120 source diagram crops are pixel-identical. All 120 actual encoded hold frames compare against the completed source at minimumSSIM0.997218, mean0.997248; the threshold is0.995. The crop includes the Config recipe, startup, container, lookup and managed-bean qualifier, while excluding captions and progress rail.

The Thanks scene starts at **41.962667s** and continues through the movie end. The actual final encoded frame2604 was checked against the source Thanks card atSSIM0.998802 Its spoken phrase matches the SRT. The large main-card lettering supplies the visible words without a duplicate lower caption band.

Actual decoded frames were inspected for mobile readability and clipping: `source/evidence/final-decoded-mobile-contact.png`, `final-decoded-scene-6.png`, and `final-decoded-scene-7.png`. Source/evidence/qa-notes.md and config-qa-review.json record review scope. Current final-* and config-* files are authoritative; earlier recap-* artifacts preserve the previous generic ending.

## Fresh actual Java verification of Config

The new companion `source/java/ConfigFlowDemo.java` was compiled and run using existing pinned ECJ3.40.0, OpenJDK21.0.13 and Spring6.2.11 dependencies. Both compilation and execution exited 0 with empty stderr. Actual stdout:

```text
App starts Spring with Config.class
Spring instantiates Config
Spring calls Config.repo(): create Repo
Spring calls Config.service(repo): wire Repo into Service
Spring context is ready
App calls getBean(Service.class)
same Repo bean: true
App calls getBean(Service.class) again
same Service bean: true
factory calls after lookups: 2 (unchanged)
```

Assertions verify factory order and that both factories execute during startup, before the ready context is returned and before application lookup. Repeated default-singleton lookups do not invoke the factories again. This is the concrete behavior represented by the new ending. Run `bash source/java/run-config-flow.sh`; see source/java/config-flow-notes.md and source/evidence/config-java-*.

The earlier `IoCDemo.java` and its runner are unchanged. Their original actual identity checks still back the scene 5 excerpt `spring wiring: true`: the Service holds the same Repo bean returned by the container. An independently constructed Repo remains a different object. Spring manages registered beans, not all Java objects.

Official documentation retained in source/evidence/java-*:

- https://docs.spring.io/spring-framework/reference/core/beans/introduction.html
- https://docs.spring.io/spring-framework/reference/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html

## Narration and listening limit

Local Kokoro v1.0 float32ONNX uses the same80%am_puck/20%am_fenrir male style blend at speed1.02, without pitch shifting, time stretching, external speech service or replacement TTS. Each of seven scenes fits one inference batch. First five scene durations remain unchanged.

Narration is 43.403417s,48kHz mono PCM24; onset0.015250s, peak-1.514414dBFS, RMS-21.123701dBFS, zero clipped samples and zero endpoint samples. Quiet-edge4ms microfades prevent edit clicks. Voiced pitch10th/50th/90th percentiles are 86.84/111.96/171.08Hz, with 4.80semitones variation.

Independent unprompted Whisper base.en recognizes all **99 normalized words**, including Config, Repo, Service and Thanks for watching. Raw normalized WER is **0.000000**; no manual transcript correction was needed. G2P inputs and raw ASR are retained. Caption/animation word anchors use approximate20ms-grid ASR timestamps; scene edit boundaries and the two-second recap pause are sample-derived. The return-reference tone occurs at37.380s; the Thanks card continues the original music fade without another effect.

**Unmet voice requirement:** automated transcript, pitch and continuity checks cannot certify smooth human delivery, perceived age or subtle synthesis artifacts. This environment has no audio-input listening capability. Perceptual acceptance remains incomplete and is not claimed. See source/voice/voice-qa.md.

## Scene times

| Scene | Actual source timeline |
| --- | --- |
| 1 | 0.000000–1.891083s |
| 2 | 1.891083–7.146625s |
| 3 | 7.146625–15.349708s |
| 4 | 15.349708–20.163375s |
| 5 | 20.163375–29.250625s |
| 6 | 29.250625–41.962667s |
| 7 | 41.962667–43.403417s |

## Rights, platform packages and reproduction

All animation, cover, Config overview, Thanks card, script, background audio and sound effects are original production material. Licensed OpenSans/DejaVu fonts and Apache-2.0 Kokoro styles are retained with notices; tools are free/open-source. Asset-rights.md and originality-review.md describe actual provenance and review limits. No paid stock, sampled music, proprietary font, named-person voice cloning or exhaustive-originality-search claim is involved.

Each actual platform MP4 is independently probed and fully decoded; it is byte-identical to the master. Covers and SRTs match their source files. Current per-export values and command logs are in source/evidence/platform-*. Both upload ZIPs include video, cover, SRT, platform copy, upload notes, technical/voice notes and checksums. YouTube also includes tags and pinned comment text. No platform posting or scheduling occurred.

`source/rebuild.sh` reproduces both Java checks, narration, rendering, technical validation and platform packaging. `checksums.sha256` covers all current requested deliverables and source/evidence outside virtual environments/model caches/bytecode, excluding itself. Model hashes are retained separately. The complete production ZIP includes the current seven-scene lesson, recap/Thanks PNGs, reproduction files, rights and evidence. Both platform ZIPs have separate archive hashes. Previous revisions remain in Git history; the repository AGENTS.md persists the user's future-generation preferences.
