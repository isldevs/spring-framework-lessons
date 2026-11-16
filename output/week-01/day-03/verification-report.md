# Bean registration — verification report

**Encoded master and both platform copies: technical validation PASS. Overall strict completion: INCOMPLETE because the required auditory voice review is unavailable.**

An actual narrated MP4 and licensed local male Kokoro WAV are delivered. No listening approval is claimed for human naturalness, pronunciation, perceived younger-to-middle adult age or subtle synthesis artifacts. Automated recognition and signal measurements cannot substitute for that review. No fallback TTS or automatic platform publication was used.

## Approved curriculum and publication metadata

Exact topic **Bean registration**, Week01 — Spring IoC Foundations, Day3 Wednesday. Publication date remains **2026-11-18**; proposed time remains **19:00 Asia/Phnom_Penh**, UTC+07:00, equivalent to12:00UTC. These are prepared metadata, not an actual scheduled post. Public media/copy contain no week/day/episode numbering. `source/production-settings.json` retains the approved inputs. The earlier different-topic Day3 files remain in Git history at d05b1a3; the current directory implements the approved topic.

## Actual encoded master

| Property | Actual result |
| --- | --- |
| Duration | **38.400000s**, within35–40s and strictly below45s |
| Picture | Native1080×1920, progressive H.264, yuv420p8-bit |
| Frame rate/count | Constant60/1FPS;2304decoded frames and2304timestamps checked |
| Color | Rec.709 matrix/transfer/primaries, limited/tv range, SDR |
| Audio | AAC stereo,48000Hz; stream duration38.387s |
| Narration WAV |38.387208s,48000Hz mono PCM24 |
| Encoded loudness | −15.81LUFS integrated, −0.87dBTP true peak,3.60LU range |
| Scenes/subtitles |7scenes;18SRT cues, maximum35characters |
| Full decode | Exit0 with empty FFmpeg error log |
| Black intervals |0detected with retained settings |

Master SHA-256:

```text
b4ca78bb820dd008a9b598b525dc4041353e0bf49007f006b2f76bee28eb63b9  video.mp4
```

Raw FFprobe output, commands, stdout/stderr, assertions and hashes are retained under `source/evidence/final-*`; see [final-summary.json](source/evidence/final-summary.json). Audio is sample-derived; picture ends12.792ms later on its next60FPS boundary, retaining the quiet Thanks card without black frames.

## Genuine Java/Spring compilation and testing

Actual Spring Framework **6.2.11** runs on OpenJDK **21.0.13**. Eclipse ECJ **3.40.0** compiles Java17-target classes; Maven, javac and Spring Boot are not used. Ten pinned compiler/runtime/test jars have Maven Central provenance, verified hashes and retained licenses/notices. JUnit Jupiter5.12.2 / console platform1.12.2 executes the tests.

**3JUnit tests passed,0failed.** Main compilation, test compilation, JUnit and the standalone RegistrationDemo all exited0 with empty stderr.

1. A refreshed context without Client registration has no client definition or singleton. getBean(Client.class) throws the expected NoSuchBeanDefinitionException, and no Client constructor runs. This proves the missing-bean failure is registration-related rather than an unrefreshed context.
2. The application registers FactoryConfig and refreshes. A BeanFactoryPostProcessor observes a client BeanDefinition with factoryConfig/client factory metadata before any Client singleton or factory call. Spring then invokes the @Bean method once. Typed/named repeated retrieval returns the same Client, with one candidate, one constructor and one factory call.
3. Registered ScanConfig configures @ComponentScan("lesson.scan"). The Worker class definition is observed before its constructor. Worker is retrievable and reused as the same default singleton. Outside has @Component but lives in lesson.outside; its definition is absent, its lookup throws the expected missing-bean exception and its constructor never runs.

Actual standalone proof includes:

```text
plain class missing: true
@Bean definition: client
@Bean factory called
Client created
@Bean retrieved: true
scan definition: worker
Worker created
scan retrieved: true
outside scan missing: true
```

JUnit additionally captures `@Bean definition before instance: true` and `scan definition before instance: true`. Logs, exact commands, exit codes, XML and source hashes substantiate these results in [java-verification-result.json](source/evidence/java-verification-result.json). The media validator independently checks current source hashes against the tested hashes and verifies the four displayed outcome lines in actual application stdout; it does not claim to rerun Java.

The successful paths use separate contexts and default non-lazy singletons. Pictures illustrate selected application definitions, while infrastructure/configuration registrations also exist. Both demonstrated paths create BeanDefinitions before their instances; other registration APIs, including direct singleton registration, are outside this focused comparison. The script therefore says to give Spring a registration path rather than claiming every Spring bean must have a BeanDefinition or that these are the only possible routes.

Eight official Spring pages were actually retrieved with HTTP200; source URLs, resolved URLs, response hashes, HTML/text and claim excerpts remain under `java-doc-*`. References include [@Bean6.2 reference](https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html), [component scanning6.2 reference](https://docs.spring.io/spring-framework/reference/6.2/core/beans/classpath-scanning.html), and [AnnotationConfigApplicationContext6.2.11 API](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/annotation/AnnotationConfigApplicationContext.html). Both public publishing links were separately fetched HTTP200; evidence is in `publishing-reference-check.json`.

## Hook, meaningful animation and mobile inspection

The requested question is shortened for spoken pacing to **“Why isn't this a Spring bean?”** A plain Java Client class and missing Spring registration are visible from frame one. Its complete synthesized utterance lasts1.486333s; raw ASR recognizes its final word by1.04s. Narration exceeds−60dBFS at0.015104s. The first two encoded seconds measure−15.58dBFS RMS.

The core opening has100unique sampled frames, with the first visual change at1/60s. Five actual encoded opening snapshots at0/.25/.5/1/2s match corresponding source frames with minimum SSIM0.998607. No greeting, logo intro, fade, static cover/title hold or black opening delays the hook. A separate1080×1920 cover PNG is delivered.

Explanatory animation anchors:

- Missing lookup request1.956333s → verified missing result4.460s.
- Registered factory configuration8.966292s → definition12.160s → factory call12.880s → Client15.520s → lookup15.920s.
- Configured scan19.500s → definition19.620s → Worker19.880s → complete graph20.230s → lookup21.265917s.
- Annotated outside-package class remains missing at26.060s.

These anchors explain causal ordering and are not measurements of Spring execution speed. The factory lookup/FOUND display remains visible1.011125s before its cut, and the scanned lookup1.50s. Actual decoded transition frames confirm both positive states after their instances exist.

The production agent inspected actual decoded opening, all seven scene stills and all six transition pairs at mobile scale. No clipped labels, caption collisions or crowded diagram connections were observed. All250source safe-bound samples passed X=90..990,Y=250..1520 for important bright content; an additional217state preflight passed. [Visual-review scope](source/evidence/visual-review.md) distinguishes these checks from physical-phone playback or continuous human viewing.

All18SRT cues match the final narration/timeline with documented annotation/compound formatting. Captions are burned into the picture from the opening hook. The final overview merges the registered @Bean/configured component-scan paths through definitions to managed beans/getBean, alongside actual proof and one takeaway. It holds complete **34.679125–36.679125s**, exactly2s before separate spoken Thanks. All120source hold samples are pixel-identical in the diagram crop; all120encoded comparisons pass with minimum SSIM0.997991. Actual last frame2303 matches the Thanks source with SSIM0.998690.

## Voice, audio continuity and remaining review

Local Kokoro v1.0 uses80%am_puck/20%am_fenrir male English styles, one coherent inference batch per scene. Hook model speed is1.00, body0.80. An earlier ambiguous component phrase was independently transcribed, then replaced by a complete coherent utterance: “Or add the component annotation, then scan the package containing your class.” No word-level voice splicing, waveform stretching, pitch shifting or substitute TTS is used.

Raw unprompted full-stream Whisper base.en recognition has **72expected/73recognized words, edit distance2, WER0.027778 (2.7778%)**. The discrepancy is `classpath` versus `class path`. The raw result remains intact; compound timing spans and @Bean/@Component display formatting are documented separately. Known sample-derived utterance boundaries take precedence over ASR drift across the silent reading hold. No expected words or listening result were silently fabricated.

Clean WAV peak is−1.514415dBFS, with0clipped samples and zero-valued endpoints. Median voiced F0 is115.24Hz, with3.88semitones variation; those measurements do not establish perceived age or naturalness. Quiet joins use4ms microfades. The longest pre-hold source quiet interval is0.675875s between phrases.

Original Python/NumPy A-minor-add9 harmonic audio and five timed registration cues are mixed beneath narration with speech ducking and measured two-pass normalization. The final−50dBFS/150ms silence scan detects only the intended quiet tail from38.1985s. Full decoding, source endpoints and retained mix/silence/loudness evidence support technical continuity; subtle auditory artifacts cannot be certified without listening.

## Packages, rights and status

Both platform MP4s were independently FFprobed and fully decoded with exit0 and empty error logs. Each2304frame copy equals the master SHA-256 above; each packaged cover and SRT equals its current master asset. Platform folders contain their own metadata/hashtags, phone-ready text, technical notes, FFprobe output and checked manifests. [Platform validation](source/evidence/platform-validation-summary.json) records these actual results. Upload ZIPs pass CRC checks; the final delivery audit checks the complete production ZIP and every archived member as well.

[Asset rights](asset-rights.md) and [originality review](originality-review.md) retain provenance and license evidence. Production uses free/open-source tools, procedural graphics and original synthesized audio, with no stock footage or sampled song. No exhaustive plagiarism screening or worldwide novelty claim is made. Reproducible Java/tests, Pillow/NumPy sources, dependency records and Kokoro setup are included; downloaded speech models, environments and Python bytecode are excluded.

**Remaining essential requirement:** actual auditory acceptance of smooth human explanation, pronunciation, perceived male age and subtle synthesis artifacts. This runtime cannot ingest the audio for that review. The narrated MP4 and technical verification are delivered, but strict overall approval remains incomplete for that reason. Nothing was uploaded, scheduled or published to YouTube or Facebook.
