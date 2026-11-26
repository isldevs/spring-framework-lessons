# Timed storyboard — Constructor injection

Approved publication2026-11-23, proposed19:00Asia/Phnom_Penh. Scene indexes below are editing notes only and must never appear as public week/day/lesson/episode numbering. Final audio source is36.261917s; source-derived picture ceiling is36.266667s/2176frames at60FPS. Actual encoded FFprobe results are authoritative.

## Seven purposeful scenes

| Internal scene | Actual edit interval | Technical cause/effect |
| --- | --- | --- |
| 1 | 0.000000–1.835125s | Complete thumbnail and spoken hook; subtle gateway/constructor motion. |
| 2 | 1.835125–8.671500s | Spring-managed service, one constructor and optional annotation. |
| 3 | 8.671500–14.807000s | Parameter type resolves to the sole managed PaymentGateway candidate. |
| 4 | 14.807000–19.513125s | The exact gateway reference is supplied through the constructor and retained. |
| 5 | 19.513125–25.786708s | Service execution delegates to the injected gateway; actual JUnit proof/result is revealed. |
| 6 | 25.786708–34.921167s | Manual-new boundary and progressively completed configured injection overview. |
| 7 | 34.921167–36.261917s | Separate Thanks for watching card after the reading hold. |

## Opening and thumbnail composition

At00:00the full1080×1920cover composition is already visible. White heavy Inter typography is left-aligned in three lines: “Spring Injection”; “No @Autowired?” on the rounded blue#0866FF keyword highlight; “It still works.” Actual per-line sizes are104/96/104px at Inter weight900; the blue line is96px to preserve full safe-area padding. The glyph union isX110..929/Y499..879. The headline remains recognizable/stable through the first second. The dark-navy technical background shows the Spring-managed OrderService constructor and gateway dependency, rather than a decorative stock image. Brand text is small. Headline, supporting code and caption region remain separate inside conservative safe margins.

The independent opening caption is exactly “No Autowired? This still works.” from0–1.755125s. It is required because the headline contains different words. All headline words are visible from frame0; narration and subtle dependency motion begin immediately. From1–2s, a highlighted constructor/code element moves into the mechanism explanation while the headline transitions smoothly. No silent title card, logo intro, greeting, black frame or fade to black is inserted. Actualsource cover equality, decoded first-frame similarity and samples0/.5/1/2s are quality gates, not presumed successes.

## Mechanism and qualification

Config imports OrderService and DemoPaymentGateway. The service has exactly one constructor with no@Autowired; Spring selects it implicitly. Its PaymentGateway parameter is a type request. With one registered matching candidate, Spring resolves the managed gateway and passes that reference through the constructor. The object remains the same instance, rather than being copied into a second gateway. Calling placeOrder(2500) delegates to the in-memory demo and returns the actual verified string demo-paid:2500.

Actual proof snippets come from executed JUnit output: constructors:1, autowired:false, gateway same:true, order result:demo-paid:2500 and manual uses caller:true (raw output retains spaces after colons). There are2actual passing tests. No fabricated terminal output, real payment, standalone application execution or comprehensive behavior coverage is represented.

The manual path makes caller ownership explicit: `new OrderService(manualGateway)` receives the argument supplied by the caller. The diagram must not show Spring injecting arbitrary objects created with new. The recap connects configured managed beans, constructor selection, type/candidate resolution, reference supply and verified service use. Default singleton behavior and this selected context are the demonstrated contract; other constructor/candidate cases are not generalized.

## Final audio-linked edit anchors

| Cue | Absolute edit time |
| --- | --- |
| managed.one | 3.340000s |
| managed.select | 4.880000s |
| managed.optional | 7.340000s |
| resolve.parameter | 10.760000s |
| resolve.search | 11.960000s |
| resolve.match | 12.880000s |
| inject.supply | 15.100000s |
| inject.store | 18.020000s |
| inject.ready | 19.040000s |
| execute.call | 20.240000s |
| execute.result | 22.140000s |
| execute.instance | 23.280000s |
| execute.verify | 25.250000s |
| recap.manual | 27.020000s |
| recap.load | 30.320000s |
| recap.resolve | 30.640000s |
| recap.supply | 31.240000s |
| recap.execute | 31.780000s |
| recap.complete | 32.330000s |

The complete recap is then held **32.921167–34.921167s**, exactly2s, before the Thanks card at34.921167s. Captions follow final source/sample boundaries and approximate local-ASR word spans. Event cues show explanatory order and are not measurements of Spring/JUnit wall-clock performance.

## Caption and image QA

Use52pxInterBold white text, centered near540/1380, on a text-width-following rounded black82%RGBA panel. Padding26pxhorizontal/14pxvertical; corner radius12px; maximum840pxwidth; normally one line, no more than two. Measure real glyph bounds with textbbox and alpha-composite the panel. Keep the entire rectangle insideX90..990/Y250..1520. Wrap coherent phrases instead of shrinking text. The opening title/blue highlight, code, diagrams and captions must not overlap. No karaoke, bouncing, flashing or distracting caption animation.

Verify the cover and first-frame composition using the actual PNG/source frame before compression and suitable decoded-image similarity afterward. Inspect0.5/1/2s samples, the stable first-second headline, transition continuity, small-feed and likely1:1/3:4profile crops. These are preview/crop checks, not a guarantee of a platform's current crop or automatic thumbnail choice. First-frame.png andqa/hold the actual encoded evidence and mobile previews.

Inter weight, headline sizes, highlight padding/rounding, actual glyph bounds and caption settings belong in the renderer's thumbnail-style.json/subtitle-style.json and font provenance. Actual safe-bound/rendered-media results and limitations belong in verification-report.md. No physical-phone, browser-playback or auditory acceptance is claimed without a genuine review. Manual thumbnail/cover/AI-label checks remain in the platform metadata and platform-policy-review.md.
