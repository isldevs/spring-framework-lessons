# Bean naming — verification report

**Encoded master and both platform copies: technical PASS. Overall strict approval remains INCOMPLETE because auditory voice acceptance is unavailable.** Actual licensed local male Kokoro narration is delivered. No listening review or approval of human naturalness, final pronunciation, perceived age or subtle artifacts is claimed.

## Approved lesson and publication plan

Topic **Bean naming**, publication date **2026-11-20**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC) are preserved. Week01/Day5 identifiers remain internal. No upload, scheduling or publication occurred. The earlier unfinished Day4 files were preserved outside this production's edits and are not represented as completed by this report.

## Actual encoded artifact

| Property | Measured value |
| --- | --- |
| Duration | **39.300000 seconds**, within35–40 and strictly below45 |
| Picture | Native1080×1920, progressive H.264, yuv420p8-bit |
| Rate/count | Constant60FPS;2358decoded frames and2358timestamps checked |
| Color | Rec.709 matrix/transfer/primaries, limited range, SDR |
| Audio | AAC stereo,48000Hz; stream duration39.286s |
| Clean narration |39.286167s,48000Hz mono PCM24 |
| Loudness | −15.89LUFS integrated, −1.37dBTP true peak,2.60LU range |
| Structure |7scenes,23SRT cues, maximum35characters |
| Full decode | Exit0, empty FFmpeg error log |
| Black intervals |0detected with retained settings |

Master SHA-256:

```text
3b882122e03afd42b9505b6e7f570741719c3704f86ca11b1453ee92584c9c83  video.mp4
```

Actual FFprobe, commands, stdout/stderr, frame comparisons and hashes remain in `source/evidence/final-*`. [final-summary.json](source/evidence/final-summary.json) is the measured machine record. Picture ends about13.83ms after source audio on the next60FPS boundary, retaining the quiet Thanks card.

## Genuine Java/Spring verification

Actual Spring Framework6.2.11 runs on JDK21.0.13. Eclipse ECJ3.40.0 compiles Java17-target classes; Maven, javac and Spring Boot are not used. Ten pinned compiler/runtime/test jars have checked Maven Central provenance/hashes and retained license notices. JUnit Jupiter5.12.2 / console platform1.12.2 executes the tests.

**4JUnit tests passed,0failed.** Main compilation, test compilation, JUnit and the standalone NamingDemo all exited0 with empty stderr. The four tests verify:

1. Explicit @Bean("alpha") registers a bean named alpha while its factory method is client. The method name is not an extra registered name. Named lookup, named-plus-type lookup and type-only lookup all return the same default singleton in the single-Client context.
2. A fresh context registers alpha and beta as two distinct Client instances. Neither is primary. Both named lookups work; getBean(Client.class) throws NoUniqueBeanDefinitionException with exactly two named candidates, alpha and beta.
3. getBean("alpha", String.class) throws BeanNotOfRequiredTypeException with the actual/required classes recorded. The name selects a bean and the extra type argument checks that selection; it is not the same operation as getBean(Client.class).
4. A separate constructor parameter annotated @Qualifier("beta") receives beta. Direct getBean(Client.class) remains ambiguous in that context. Qualifier-based injection selection and named lookup are distinct mechanisms.

Actual standalone output:

```text
named alpha: alpha
typed name alpha: alpha
single type same: true
named beta: beta
type lookup: NoUniqueBeanDefinitionException
type candidates: 2
```

The actual exception message also records the two candidates alpha,beta. Logs, commands, exit codes, XML and source hashes are retained in [java-verification-result.json](source/evidence/java-verification-result.json). The media validator checks current Java hashes against the tested sources and the six proof lines against actual stdout; it does not claim to run Java again.

The single-Client and two-Client examples use separate contexts. In the two-Client case initialization succeeds and the expected failure comes from a later lookup. The video preserves the ready context while highlighting the failed type query. The pictured area illustrates selected Client beans, not every configuration/infrastructure bean. alpha and beta identify two different objects, not two aliases for one object. Client.id is a demo marker assigned explicitly by the factory, not a field automatically populated by Spring naming.

The ambiguity is scoped to this example without a primary or other selection preference. Names alone do not resolve every type ambiguity; this report does not claim every multi-candidate lookup fails. Qualifiers narrow type-driven injection candidates and can use bean-name fallback matching; that does not make getBean(name) a qualifier annotation.

Seven unique official Spring reference6.2/API6.2.11 pages were actually retrieved HTTP200, with resolved URLs, hashes, HTML/text and supported excerpts under `java-doc-*`. References include [@Bean naming](https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html), [BeanFactory lookup APIs](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/BeanFactory.html), and [qualifier semantics](https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired-qualifiers.html). Both public publishing links were separately fetched HTTP200; `publishing-reference-check.json` preserves that evidence.

## Opening, synchronization and visual inspection

The original hook was refined for accuracy and spoken pacing to **“Two names. One ambiguous type.”** Its coherent utterance lasts1.787625s; raw ASR recognizes its last word by1.40s. Source narration crosses−60dBFS at0.015s. The first two encoded seconds measure−16.77dBFS RMS.

The first frame presents two distinct Client objects, their names and a type-only request. Core motion begins at1/60s;114sampled opening core frames are unique. Five actual encoded opening snapshots at0/.25/.5/1/2s match their corresponding source frames with minimum SSIM0.998684. There is no greeting, logo intro, static cover/title hold, fade or black opening. The branded1080×1920 cover is a separate PNG.

Explanatory edit anchors: explicit name4.20s/definition4.30s/first instance4.65s; named request8.70s/return9.00s/type guard11.92s; single-type lookup15.70s/return16.00s; fresh two-bean configuration18.94s/second instance19.91s/complete graph20.26s; ambiguous type query23.76s/failure24.06s. These are explanatory animation timings, not Spring execution benchmarks.

The production agent inspected actual decoded opening frames, all seven scene stills, before/after all six cuts, and the actual single-type-success anchor at mobile scale. No clipped labels, caption collisions or crowded connectors were observed. All254source safe-bound samples pass X=90..990,Y=250..1520 for important bright content; a separate217state preflight passes. The single-type query connector is routed around the context header, and configuration labels are right-aligned inside the safe area.

The final overview compares a named selection against this ambiguous type-only query, with genuine proof lines. It remains complete for **35.945417–37.945417s**, exactly2s before a separate narrated Thanks card. All120source hold samples are pixel-identical in the diagram crop; all120encoded comparisons pass with minimum SSIM0.998170. Actual last frame2357 matches the Thanks source with SSIM0.999171. [Visual-review scope](source/evidence/visual-review.md) distinguishes these checks from continuous viewing on a physical phone.

## Narration, captions and audio continuity

Local Kokoro v1.0 uses80%am_puck/20%am_fenrir male English styles, all seven coherent scene batches at1.02. Ordinary joins are0.08s; the complete-overview hold is2s and final tail0.25s. No waveform time stretching, pitch shifting, word-level voice splicing or substitute TTS is used. The final script contains97normalized words.

Actual unprompted full-stream Whisper base.en recognizes **97/97words, edit distance0, WER0**. Raw ASR and timestamps remain intact. Twenty-three captions match the final script and sample-derived scene edits; intermediate word timing uses approximate20ms ASR estimates. No expected speech words were silently inserted. Punctuation/case in Java terms is display formatting, with provenance retained.

Clean WAV peak is−1.514415dBFS, with0clipped samples and zero-valued endpoints. Voiced median F0 is113.26Hz with4.63semitones variation. The refreshed source−45dBFS/120ms scan finds the longest pre-hold quiet interval0.507896s. Quiet joins use4ms microfades. Model/voice checksums, phonemes, licenses and reproduction inputs remain in `source/voice/`; temporary model links and large speech caches are excluded.

Original NumPy E-minor-add9 harmonic audio and five meaningful lookup cues are mixed beneath speech with ducking and measured two-pass normalization. The encoded−50dBFS/150ms silence scan detects only the intended final quiet tail from39.121396s. Full decoding and retained source/mix/loudness logs support technical continuity. These objective checks do not establish perceived human naturalness, voice age or every pronunciation detail.

## Packages, rights and remaining requirement

Both current platform copies were independently FFprobed and fully decoded with exit0 and empty error logs. Their2358frame MP4s equal the master SHA-256 above. Each packaged cover and SRT is byte-identical to its current master asset. Platform manifests, paste-ready text, technical notes and raw checks are retained in [platform-validation-summary.json](source/evidence/platform-validation-summary.json). Upload ZIPs pass CRC checks; finalization additionally checks every production-ZIP member and refreshes archive hashes.

[Asset rights](asset-rights.md) and [originality review](originality-review.md) document actual commercial-use provenance and review limits. Production uses free/open-source tools, procedural graphics and original synthesized audio. No exhaustive plagiarism search or worldwide novelty certification is claimed. Java/tests, animation/audio/voice generation source, locks, dependency notices and model hashes are included; environments, downloaded speech models and Python bytecode are excluded.

**Remaining essential requirement:** actual auditory acceptance of smooth human explanation, pronunciation, perceived younger-to-middle adult male age and subtle artifacts. This runtime cannot ingest audio for listening review. All technical media and package checks above are actual, but overall strict approval remains incomplete for that reason. No YouTube/Facebook upload, scheduling or publication occurred.
