# Constructor Injection in Spring Boot — verification report

**Rendered master and both platform copies: technical PASS. Overall strict completion: INCOMPLETE — the required perceptual voice review cannot be performed in this runtime.**

Actual local Kokoro male narration is delivered. No auditory listening approval is claimed for perceived younger-to-middle adult age, smooth human explanation, subtle synthesis artifacts or every aspect of pronunciation. ASR, pitch, silence and loudness measurements do not establish those qualities. No fallback TTS was substituted. Nothing was uploaded, scheduled or published to YouTube or Facebook.

## Actual encoded artifact

| Property | Measured result |
| --- | --- |
| Container duration | 35.833333 seconds; within the 35–40s target and strictly below 45s |
| Picture | Native 1080×1920, progressive H.264, yuv420p, 8-bit SDR |
| Frame rate and count | Constant 60/1 FPS; 2150 decoded frames and 2150 checked timestamps |
| Color | Rec.709 matrix, transfer and primaries; limited/tv range |
| Audio | AAC, 48,000Hz, 2 channels; stream duration 35.819s |
| Clean narration | 35.819167s, 48kHz mono PCM24 WAV |
| Encoded audio loudness | −15.82 LUFS integrated, −1.23dBTP true peak, 3.20LU range |
| Scenes / separate subtitles | 7 scenes; 18 synchronized SRT cues, maximum 40 characters per cue |
| Full decode | Exit 0; empty FFmpeg error log |
| Black intervals | 0 detected with the retained blackdetect settings |

Master SHA-256:

```text
e67a50ac287f8377a3a50a05eea8a7efc5e169d4a80c7e8f2769685efb931440  video.mp4
```

Raw probe, commands, stdout/stderr and machine assertions are retained in `source/evidence/final-*`. The decisive measured record is [final-summary.json](source/evidence/final-summary.json). Video starts at timestamp zero; source narration exceeds −60dBFS at 0.015813s. Audio is sample-rounded while picture ends on its next 60FPS boundary, a 14.3ms difference at the quiet tail.

## Actual Java and Spring Boot verification

The example starts real **Spring Boot 3.5.6**, using **Spring Framework 6.2.11**, rather than relabelling a bare context. A `@SpringBootApplication` in `lesson.orders` scans `@Component DemoGateway` and `@Service OrderService`. PaymentGateway is an interface. DemoGateway is the only matching managed implementation. OrderService has one constructor accepting PaymentGateway and stores the supplied reference in a private final field with a null guard.

OpenJDK 21.0.13 executes Java17-target classes compiled with Eclipse ECJ 3.40.0. Maven and javac are not installed and are not claimed as used. The runner pins 13 jars, checks hashes and retains compiler/runtime/test notices. Versions align with the retained Spring Boot 3.5.6 BOM. Micrometer is 1.15.4, SnakeYAML 2.4 and JUnit Jupiter 5.12.2 / console platform 1.12.2.

**Actual JUnit result: 2 tests found, 2 successful, 0 failed.** Main compilation, test compilation, JUnit and the standalone Boot application all exited 0; their stderr logs are empty.

1. A Boot integration test confirms the actual Boot version, one gateway candidate, identity of the managed and injected gateway, gateway construction before the service constructor and context readiness, no charge before application use, the simulated receipt, one gateway call and singleton reuse.
2. A separate plain-Java test manually supplies a recording fake through the same constructor. It checks the forwarded order ID, amount in cents, call count and returned result. This fake is not an extra production bean.

Actual captured proof lines include:

```text
same gateway bean: true
receipt: APPROVED order-1042 USD 19.99
Spring Boot integration test: passed
fake gateway test: passed
```

These lines are backed by assertions and [java-verification-result.json](source/evidence/java-verification-result.json), raw logs, exit codes and JUnit XML. The gateway simulates approval in memory: **no payment processor is contacted and no money moves**. A final field prevents reference reassignment; it does not make the gateway object immutable. Single-constructor selection requires no `@Autowired` annotation here. Startup timing describes this default non-lazy singleton example, not every scope or lazy arrangement.

The video uses the standard valid `SpringApplication.run(CheckoutApplication.class)` startup shorthand. The executable configures a SpringApplication instance for non-web, quiet, deterministic output before calling its `run` method. Both depict Boot starting Spring and scanning the application package.

Official documentation was actually retrieved (HTTP 200), with URLs, hashes, text and relevant claim excerpts under `source/evidence/java-doc-*`:

- [Spring Boot 3.5: beans and dependency injection](https://docs.spring.io/spring-boot/3.5/reference/using/spring-beans-and-dependency-injection.html)
- [Spring Boot 3.5: SpringApplication](https://docs.spring.io/spring-boot/3.5/reference/features/spring-application.html)
- [Spring: single-constructor injection rules](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired.html)

## Opening, captions and visible mechanism

Source frames 0–59 equal the supplied cover PNG exactly, without captions, progress rail, fade or black frames. H.264 is lossy: all 60 encoded opening frames were compared against the Rec.709-converted cover, with minimum SSIM **0.998665** and average **0.998761**. The separate PNG is 1080×1920 and is selectable through the video's opening second when phone upload interfaces use a video frame as the thumbnail.

All 18 SRT texts and millisecond-rounded timestamps match the actual timeline and script words. Burned captions reserve their own band and start after the unchanged cover interval; the separate SRT starts with immediate speech. The closing card displays its own spoken words rather than duplicating a burned caption.

The constructor reference animation finishes at **15.610s**, before application order use begins at **17.180s**. Actual decoded frames at 15.71s and 17.28s were inspected at mobile size and retained in `final-causal-mobile-review.png`. These are explanatory animation anchors aligned with narration, not measurements of Spring's execution speed.

The full overview connects Boot startup/scanning → required constructor parameter and one matching implementation → supplied reference → application use. It is complete by 28.050s. Its explicit reading hold is **32.283125–34.283125s**, exactly two seconds, before the separate narrated Thanks card. All 120 source hold samples were pixel-identical within the diagram crop; all 120 encoded frames passed comparison, with minimum SSIM **0.997587**. The last encoded frame, index2149, matches the Thanks source with SSIM **0.998693**. The extra 14.3ms picture rounding retains that card.

All seven actual decoded scene stills were viewed at 360×640 scale. No clipped text, caption collisions or crowded diagram connections were observed. All 189 source safe-bound samples passed X=90..990, Y=250..1520 constraints for bright foreground content, with an additional 217-state preflight retained. See [visual review scope](source/evidence/visual-review.md). No real-time playback on a physical phone is claimed.

## Voice, synchronization and continuity

The voice is locally inferred Kokoro v1.0, **80% am_puck / 20% am_fenrir**, seven coherent scene batches at inference speed **0.90**. Model and voice hashes, phoneme inputs, license/model-card evidence, dependencies and reproduction scripts remain in `source/voice/`. No pitch shifting or waveform time stretching was used.

Clean WAV measurements: peak −1.514415dBFS, 0 clipped samples, zero-valued endpoints. Voiced median F0 is117.26Hz with4.04semitones standard deviation. Source quiet joins use4ms microfades. These are objective signal properties, not proof of perceived age or naturalness.

Unprompted full-stream Whisper base.en recognizes **74 of77 expected words**, omitting the three-word closing after the reading hold: raw normalized WER **0.038961 (3.8961%)**. That raw result is preserved. A separate unprompted transcription of the actual final audio crop recognizes **Thanks for watching**, 3/3 words. The alignment record combines independently observed times without silently inserting expected words or changing the raw score. Do not describe full-stream recognition as zero WER. Boundaries use approximate20ms ASR timing, with scene/hold edits derived from samples.

The background and event sounds are original NumPy synthesis, with speech ducking and continuous audio across scene cuts. Five quiet event tones align with final-reference declaration, gateway match, constructor passage, fake test and complete recap. The encoded mix's −50dBFS/150ms silence scan detects only the intended final quiet tail beginning35.630729s; no unexpected interior silence appears at that threshold. Source silence/ASR/pitch evidence and final encoded loudness/silence logs are retained. No listening review was performed; subtle clicks, pronunciation and human naturalness cannot be certified by these checks alone.

## Packages, rights and remaining requirement

Both platform MP4 copies were **independently FFprobed and fully decoded** with exit0 and empty error logs. Each has the master's 2150frames and measured properties, and each SHA-256 equals the master above. Both packaged covers and SRT files match their current master files byte for byte. Each folder has its own checked manifest, paste-ready platform text and review notes. [Platform validation](source/evidence/platform-validation-summary.json) records those actual results. Both upload ZIPs passed archive CRC checks during packaging; the final delivery audit also tests the production ZIP and delivery manifests.

The [asset-rights record](asset-rights.md) and [originality review](originality-review.md) retain model/font/dependency license evidence and truthful review scope. No stock footage, sampled song, paid production software, exhaustive plagiarism certification or global novelty claim is used. Reproducible Java, Pillow rendering, NumPy mixing and Kokoro setup sources are included; environments, Python bytecode and downloaded speech-model caches are excluded.

**Remaining incomplete requirement:** perceived younger-to-middle adult male age, smooth human explanation and final pronunciation/naturalness acceptance require an actual auditory review. This runtime cannot ingest the audio for that review. The actual technical deliverables are provided and pushed, but strict overall video approval remains incomplete for that reason. No platform publication was performed.
