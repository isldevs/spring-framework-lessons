# Verification report — How Spring Dependency Injection Works

**Actual video, Java verification, encoded technical checks and platform packages: produced and verified. Overall strict completion: INCOMPLETE because perceptual voice acceptance is unavailable.** This environment cannot ingest audio for a listening review. Perceived age, smooth human naturalness and subtle synthesis artifacts have not been auditorily accepted. No listening result is fabricated and no replacement TTS was used.

Production schedule is2026-11-17; week/day identifiers remain internal file organization and are absent from footage and publishing copy. Nothing has been uploaded, scheduled or published to YouTube or Facebook. GitHub delivery is separately authorized by the user.

## Actual encoded master

| Check | Measured result |
| --- | --- |
| Duration | 35.650000 s; within35–40 s and strictly below45 s |
| Resolution | Native 1080×1920 portrait, progressive |
| Rate and frames | Constant 60FPS; 2,139 actual decoded frames |
| Codecs | H.264 High / AAC LC stereo 48,000Hz |
| Color | yuv420p 8-bit SDR, limited/TV range; BT.709 matrix, transfer and primaries |
| AAC duration | 35.650000 s |
| Full decoding | FFmpeg exit0, empty error log |
| Presentation timestamps | All 2139 checked, zero start and1/60 s increments |
| Encoded loudness | -15.86LUFS, -1.37dBTP, 2.80LU loudness range |
| Continuity | No internal dropout at−50dBFS/150ms; intentional final quiet tail starts35.428792 s |
| Black scan | No black intervals detected |
| Captions | 16 synchronized positive-duration cues, ordered/nonoverlapping/inbounds; words match exact script; maximum43characters |
| Safe area | 188 source states pass X90..990/Y250..1520 |

Final master SHA-256:

```text
5aa13ce8c9dab3ec4d24cb32a188cb495ef8632ba85752281a64c75b72cdfa28
```

Raw FFprobe output, commands, full decode, frame timestamps, audio/black scans, screenshots and digest are retained under `source/evidence/final-*`. `final-summary.json`, `qa-notes.md` and `qa-review.json` record actual results. The same verified master was copied losslessly into both platform packages; the exports were probed and fully decoded separately.

## Actual Java/Spring execution

Pinned Spring Framework6.2.11 ran on OpenJDK21.0.13; ECJ3.40.0 compiled Java17-target class files because this environment has a Java runtime without javac. Dependency hashes were checked. Compilation and execution both exited0 with empty stderr. Actual stdout:

```text
App starts Spring with Config.class
definitions registered: repo, orderService
Repo created
OrderService constructed with Repo
context ready
same Repo bean: true
application result: ready
scanned definitions: repo, orderService
```

The package `lesson.di` contains `@Configuration Config` with `@ComponentScan("lesson.di")`, `@Repository Repo`, and `@Service OrderService`. The only OrderService constructor takes `Repo repo`; it stores that supplied reference and has no @Autowired annotation. There is exactly one matching Repo candidate.

Startup creates an empty AnnotationConfigApplicationContext, registers Config.class, then calls refresh(). A diagnostic BeanFactoryPostProcessor observes the registered definitions without requesting any bean. This directly verifies that definition registration precedes singleton constructors. Repo construction precedes OrderService construction; the context is ready before application lookup and business use. Assertions verify that `service.repo()` is the same instance as `ctx.getBean(Repo.class)` and that the injected service reaches the repository to return ready. Default singleton lookup does not rebuild the graph.

This is constructor injection from scanned stereotype classes, not a user-defined @Bean factory-method example. The video distinguishes hollow definition cards from filled runtime objects, unique Repo-type resolution, reference passage into the constructor and subsequent application use. It does not claim every Java object is a bean, that arbitrary packages are scanned automatically, or that all scopes/lazy beans eagerly initialize at startup.

Reproduce with `bash source/java/run.sh` (or `python source/java/verify.py` for separated raw provenance). Sources, fixed jars, hashes and license notices remain in `source/java/`; actual compile/run commands, output, exit codes and source hashes are in `source/evidence/java-*`.

Official Spring documentation was fetched successfully and saved with source URLs and excerpts:

- https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html — configured scans, stereotypes and BeanDefinition registration.
- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired.html — a single constructor is used even without @Autowired.
- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html — type-driven candidate matching and disambiguation scope.
- https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html — container-supplied dependencies during bean creation.

## Dependency graph chronology, cover and closing

Video graph assembly completes at **17.06s**, before application business use at **22.84s**. These are animation timestamps aligned to speech, not wall-clock Java execution durations. `final-graph-use-order.json` and actual decoded anchor frames corroborate the visual ordering; the Java trace independently verifies the corresponding runtime sequence.

The exact1080×1920cover.png is used unchanged as source frames0–59, with no fade-in, initial black frame or extra overlay. Narration starts immediately. All 60 decoded opening frames were compared with the equivalent Rec.709 cover conversion: meanSSIM0.998915, minimum 0.998874. Differences are ordinary lossy H.264 compression. The user can select the first frame/opening second as a phone-upload thumbnail.

The complete scan→register→resolve→inject→use overview is held for exactly2.0seconds, **32.209083–34.209083s**. All 120source diagram crops are pixel-identical. All 120actual encoded hold frames exceed the0.995SSIM threshold: minimum 0.998031, mean 0.998094. The crop includes the configured scan, registered definitions, constructor type and injected graph, excluding captions/progress rail.

A separate spoken **Thanks for watching** card follows the hold at34.209083s. The actual last encoded frame2138 matches its source atSSIM0.998781. The main card supplies the visible closing words without a duplicate caption band; the separate SRT retains its synchronized cue.

Inspected actual decoded seven-scene contact sheet and graph/use/thanks frames at phone scale. Core scan/constructor/lookup code, object names and captions are readable; no primary clipping or crowding was observed. Small status labels are supplementary to larger labels and narration. `recap.png` and `thanks.png` are also delivered as standalone full-resolution images. No public day/week/lesson/episode numbers or unrequested footer slogan are present.

## Narration checks and remaining blocker

Local Kokoro v1.0 float32ONNX uses the saved80%am_puck/20%am_fenrir American-English male style blend at speed1.02. All seven scene texts fit one inference batch; no pitch shift, waveform time stretch, external speech service or fallback TTS is used. Both model/voice hashes were rechecked and commercially permitted licensing evidence is retained.

Source narration is 35.649833s,48kHz mono PCM24. First signal above−60dBFS occurs at0.016667s. Peak-1.514415dBFS, RMS-20.677608dBFS; zero clipped samples and zero endpoints. Quiet edit boundaries use4ms microfades. Voiced pitch10th/50th/90th percentiles are89.38/117.26/173.67Hz, with4.31semitones variation. These metrics do not establish human naturalness or age.

Unprompted Whisper base.en full-stream decoding recognizes the first70lesson words exactly but omits the late three-word Thanks phrase after the deliberate pause. Its raw score remains **70/73 words, three deletions, normalized WER0.041096 (4.1096%)**. This is NOT reported as zero WER. A separate unprompted decoding of the actual final audio crop recognizes **Thanks for watching**, all3/3words. `supplemental-asr.json` preserves that result and absolute word times; `asr-alignment.json` combines observed timings without silently inserting words or changing the full-stream score.

Combined recognition supports intelligibility of all73script words. Word/caption anchors are approximate20ms-grid ASR timings; scene edits and the two-second hold are sample-derived. Actual source silence/prosody/phoneme records are retained in `source/voice/voice-qa.md`. Sound cues use the narrated registration, type-match, reference-pass, business-use and complete-recap anchors; the original NumPy bed is ducked beneath speech and continues through cuts.

**Remaining essential quality blocker:** this runtime cannot provide actual auditory listening review. Perceived younger-to-middle adult age, smooth human explanation and subtle synthesis artifacts have not been accepted or rejected by a listener. Under the user's completion rule the production remains incomplete on that criterion despite the actual MP4, narration, source and technical verification being delivered. No robotic substitute was used and no listening result is fabricated.

## Scene timeline

| Scene | Actual source interval |
| --- | --- |
| 1 | 0.000000–2.373917 s |
| 2 | 2.373917–7.382792 s |
| 3 | 7.382792–12.970750 s |
| 4 | 12.970750–18.441708 s |
| 5 | 18.441708–25.153958 s |
| 6 | 25.153958–34.209083 s |
| 7 | 34.209083–35.649833 s |

## Rights, archives and reproduction

`asset-rights.md` identifies the real fonts, model/voice distribution, compiler/runtime dependencies and original production assets. `originality-review.md` records source provenance without claiming exhaustive plagiarism screening or worldwide uniqueness. All graphics/script and NumPy-generated music/effects are original production material or reused own-production primitives; no paid stock clip, proprietary font, sampled song or named-person voice imitation is used. Font/model/dependency licenses accompany the source. Production uses free/open-source tools.

Both current platform copies equal the masterSHA above and passed actual per-file probes/full decodes. Their exact covers and SRTs match source hashes. Current per-export evidence is under `source/evidence/platform-*`. Separate packages contain video, cover, SRT, paste-ready platform copy, upload notes, technical/voice notes and checksums; YouTube also includes comma-separated tags and pinned comment text.

Unique archives `../day-02-youtube-shorts-upload.zip`, `../day-02-facebook-reels-upload.zip` and `../day-02-production.zip` preserve the previous lesson. `source/rebuild.sh` reproduces Java, narration, graphics, encoded checks and platform packaging. Current manifests/ZIPs must be refreshed after regeneration. `checksums.sha256` covers lesson deliverables and current source/evidence except itself, virtual environments, bytecode and downloaded model caches; models have a separate verified hash manifest. No publication or scheduling occurred on YouTube/Facebook. Normal Git delivery and required inline phone-copy metadata follow the repository AGENTS.md/MEMORY.md instructions.
