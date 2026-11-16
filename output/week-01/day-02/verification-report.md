# ApplicationContext — verification report

**Technical validation passed for the encoded master and both platform copies. Overall strict completion remains INCOMPLETE: the required auditory voice review is unavailable.**

An actual narrated MP4 and licensed local male Kokoro WAV are delivered. No listening approval is claimed for human naturalness, perceived younger-to-middle adult age, subtle synthesis artifacts or final pronunciation. Automated recognition and signal measurements cannot replace that review. No other TTS was substituted. No YouTube/Facebook upload, scheduling or publication occurred.

## Approved curriculum and publication plan

Exact lesson topic: **ApplicationContext**. Internal slot: Week01 — Spring IoC Foundations, Day2 Tuesday. Original publication date: **2026-11-17**. Proposed time: **19:00 Asia/Phnom_Penh**, UTC+07:00, equivalent to12:00UTC. The date and topic were preserved; the time remains proposed. Public media and copy contain no week/day/episode numbering. `source/production-settings.json` retains the approved inputs. The earlier different-topic production remains in Git history at d3040a5; current day-02 files implement the approved topic.

## Actual master measurements

| Property | Measured result |
| --- | --- |
| Duration | **35.816667s**, within35–40s and strictly below45s |
| Picture | Native1080×1920, progressive H.264, yuv420p8-bit |
| Frame rate / count | Constant60/1FPS;2149decoded frames and2149timestamps checked |
| Color | Rec.709 matrix/transfer/primaries; limited/tv range; SDR |
| Audio | AAC stereo,48000Hz; stream duration35.812s |
| Narration source |35.812000s,48000Hz mono PCM24 WAV |
| Encoded loudness | −15.81LUFS integrated; −1.19dBTP true peak;2.80LU range |
| Scenes / subtitles |7scenes;18SRT cues, maximum36displayed characters |
| Full decode | Exit0, empty FFmpeg error log |
| Black intervals |0detected with retained blackdetect settings |

Actual master SHA-256:

```text
91335571e3011105f6aa29f8a8024ac3b4d6d929e9a547b7174cd9f32e0e7a9e  video.mp4
```

FFprobe, commands, stdout/stderr, assertions and SHA-256 evidence are retained under `source/evidence/final-*`; [final-summary.json](source/evidence/final-summary.json) is the measured machine record. Picture ends4.667ms after audio to reach the next60FPS boundary, retaining the quiet Thanks card. No black tail is present.

## Genuine Java/Spring compilation and tests

Actual **Spring Framework6.2.11**, OpenJDK21.0.13 and Eclipse ECJ3.40.0 were used. ECJ compiles Java17-target classes; Maven and javac were not used. Ten pinned compiler/runtime/test jars have verified Maven Central provenance, hashes and retained license/notices. JUnit Jupiter5.12.2 / console platform1.12.2 executes the tests.

Main compilation, test compilation, JUnit and the standalone application all exited0 with empty stderr. **2JUnit tests passed;0failed.**

1. A new no-argument AnnotationConfigApplicationContext registers Config.class and is explicitly refreshed. A BeanFactoryPostProcessor observes the repo/service definitions before either corresponding singleton exists. The test confirms Repo construction precedes Service construction and context readiness; Service receives the managed Repo; repeated getBean returns the same Service; one DemoEvent is handled; closing invokes Service's DisposableBean cleanup once, including an idempotent second close check.
2. A separate @Lazy example has a registered definition and no singleton after refresh. Its first getBean creates one instance and repeated lookup returns that instance. This verifies why a definition must not be confused with an already created object.

Actual retained proof lines:

```text
definitions before instances: true
same service: true
events handled: 1
cleanup called: true
lazy definition before instance: true
```

The standalone app also captures `bean definitions: repo, service`, `instances at definition stage: 0`, Repo/Service construction, context readiness and `service result: hello from repo`. Logs, exact commands, exit codes, JUnit XML and source hashes substantiate these results in [java-verification-result.json](source/evidence/java-verification-result.json).

The diagrams show the demo beans in the context's BeanFactory, not every infrastructure bean or every Java object. The no-argument context already installs infrastructure definitions; register adds Config metadata, while its @Bean method definitions are discovered during refresh. Eager creation and cached lookup are qualified to this non-lazy default-singleton example. Event handling is verified with this example's default multicaster, without claiming all event publication is synchronous. Cleanup is the registered singleton callback, not a claim that Java memory is instantly freed or every scope has identical destruction behavior.

Ten official Spring pages were actually retrieved with HTTP200. URLs, hashes, HTML/text and claim excerpts remain in `java-doc-*`, including:

- [AnnotationConfigApplicationContext6.2.11 API](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/annotation/AnnotationConfigApplicationContext.html)
- [BeanDefinition6.2.11 API](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/config/BeanDefinition.html)
- [ApplicationContext6.2.11 services](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/ApplicationContext.html)
- [Spring6.2 lazy initialization](https://docs.spring.io/spring-framework/reference/6.2/core/beans/dependencies/factory-lazy-init.html)

## Opening, meaningful flow, captions and ending

The hook is shortened for spoken pacing to **“What's inside ApplicationContext?”** Its generated utterance is1.963s, starts immediately, and raw ASR recognizes its final word by1.40s. Source signal above−60dBFS begins at0.015125s. The first two encoded audio seconds measure−16.42dBFS RMS.

Frame one shows definitions as paper metadata and managed objects as solid nodes, inside an identified context/BeanFactory. Animated metadata/object highlights begin immediately. All120core opening frames are unique, with the first visual change at1/60s. Five actual decoded opening snapshots at0/.25/.5/1/2s match corresponding source frames with minimum SSIM0.998836. There is no static cover/title hold, fade-in, black frame, greeting or logo intro. `cover.png` is a separate1080×1920 branded asset, as required by the newest brief.

The mechanism shows register7.556042s → refresh9.460s → application definitions11.460s → Service instance13.080s → fully drawn reference graph13.430s → lookup15.260s → returned reference15.740s. Event publication21.560s precedes close22.480s and cleanup23.480s. These are explanatory edit anchors, not measurements of Spring execution speed.

Actual decoded opening, all seven scene stills and all six transition pairs were inspected at mobile scale. No clipped labels, caption collisions or crowded connections were observed. All249source safe-bound samples passed X=90..990,Y=250..1520 for bright important content; an additional217state preflight passed. The separate SRT is synchronized to the final narration and matches all displayed words after documented Java-name formatting.

The final overview connects new context/register → refresh/definitions/objects → getBean/same Service → event/close/cleanup, alongside genuine proof lines and the takeaway. The complete graph holds **32.275958–34.275958s**, exactly2s before the separate narrated Thanks card. All120source hold samples are identical in the diagram crop; all120encoded comparisons pass with minimum SSIM0.998158. Actual last frame2148 matches the Thanks source with SSIM0.998769. See [visual-review.md](source/evidence/visual-review.md) for scope; no physical-phone playback or continuous human viewing is claimed.

## Narration, synchronization and audio continuity

Local Kokoro v1.0 uses80%am_puck/20%am_fenrir male English styles, one coherent inference batch per scene. Hook inference speed is1.00, other scenes0.90. No pitch shifting or waveform time stretching is used. Model/voice hashes, license/model-card evidence, dependencies, phoneme inputs and reproduction source are retained under `source/voice/`; downloaded models and environments are excluded.

Actual unprompted Whisper base.en full-stream recognition matches **67/67expected normalized words, edit distance0, WER0**. Raw transcript and timestamps are retained. ApplicationContext/getBean display formatting is documented. The raw short-outro timestamp drifts into the preceding silent hold; final caption boundaries use the known sample-derived synthesis edit instead. No expected words were silently inserted and no listening result was manufactured.

Clean WAV peak is−1.514414dBFS, with0clipped samples and zero-valued endpoints. Median voiced F0 is114.58Hz with4.21semitones variation; these do not establish age or naturalness. Source quiet joins use4ms microfades. The longest pre-hold source quiet interval is0.662604s between phrases, with the intentional2s reading hold separately documented.

Original NumPy C-minor-add9 harmonic audio and five quiet event cues are mixed beneath narration with continuous ducking and two-pass loudness measurement. The final−50dBFS/150ms silence scan detects only the intended closing quiet tail from35.591187s. Full decode, channel/sample-rate checks and retained signal logs support technical continuity; subtle auditory artifacts and pronunciation remain outside listening verification.

## Packages, rights and outstanding requirement

Both platform MP4s were independently FFprobed and fully decoded with exit0 and empty error logs. Both2149frame copies are byte-identical to the master SHA-256 above; packaged covers and SRTs equal their current master assets. Each platform folder has checked hashes, its own metadata/hashtags and paste-ready copy. [Platform validation](source/evidence/platform-validation-summary.json) records actual results. Both upload ZIPs passed archive CRC checks; the final delivery audit checks the complete production ZIP and every archived member as well.

[Asset rights](asset-rights.md) and [originality review](originality-review.md) record provenance and retained licenses. Production uses free/open-source tools, procedural graphics and synthesized original audio; no stock footage or sampled song is used. No exhaustive plagiarism screening or worldwide novelty claim is made. Java tests, Pillow/NumPy sources, dependency records and Kokoro setup scripts are included.

**Remaining essential requirement: actual auditory acceptance of smooth human naturalness, pronunciation, perceived male age and subtle artifacts.** This runtime cannot ingest the audio for that review, so strict overall production approval remains incomplete despite delivery of the narrated MP4 and successful technical verification. No platform publication was performed.
