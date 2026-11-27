# Timed storyboard — Dependency resolution

Approved publication: 2026-11-24, proposed 19:00 Asia/Phnom_Penh. Scene indexes are editing notes only and never appear as public week/day/lesson/episode numbering. Actual narration is 37.017958 seconds; the source-derived picture ceiling is 37.033333 seconds / 2222 frames at 60 FPS. Actual encoded FFprobe values remain authoritative.

## Seven purposeful scenes

| Internal scene | Final narration edit interval | Technical cause and effect |
| --- | --- | --- |
| 1 | 0.000000–1.684167s | Complete thumbnail and exact spoken hook. A constructor type request moves toward the bean factory while the headline stays readable. |
| 2 | 1.684167–6.918542s | OrderService's constructor parameter becomes a required PaymentGateway dependency request. The opening transition finishes at 2s. |
| 3 | 6.918542–14.664042s | The factory discovers two compatible types; the unrelated same-named logger is excluded; candidate eligibility removes the disabled backup from autowiring. |
| 4 | 14.664042–20.001000s | One eligible gateway remains. Its existing reference is supplied through the constructor and retained in the service field. |
| 5 | 20.001000–25.823083s | A fresh MissingConfig context has no eligible candidate. The required constructor edge cannot be satisfied and refresh fails. |
| 6 | 25.823083–35.677208s | Actual JUnit proof appears, other selection rules are acknowledged, then the complete register/refresh → match → filter → inject overview is held for reading. |
| 7 | 35.677208–37.017958s | Separate “Thanks for watching” ending after the full 2-second overview hold. |

## Opening and thumbnail composition

At exactly 00:00, the full 1080×1920 cover is present. Three left-aligned heavy white Inter lines read “How Spring”, “Finds Your” and “Dependencies”. Actual weight is 900 and all three lines are 104px. Only “Dependencies” uses the rounded blue #0866FF keyword highlight, radius 20px and padding 18px horizontal / 8px vertical. The glyph union is X110..851 / Y499..899; the highlight is X110..869 / Y793..907. Small iSLDevs branding sits above. Topic-specific constructor code and a moving type request support the composition without a stock portrait or decorative slogan.

The headline differs from the spoken words, so the opening caption is separately and exactly “How does Spring know what to inject?” It occupies 0–1.604167 seconds and wraps into two coherent lines in its reserved lower region. All headline words are visible from frame zero. The headline remains stable through 1 second while the dependency request moves. From 1–2 seconds, the constructor card travels into the technical explanation as the large headline retires and the smaller scene heading appears. No greeting, silent title hold, logo intro, black frame or fade to black is inserted.

## Runtime mechanism and qualification

SuccessConfig imports the Spring-managed OrderService and registers eligibleGateway, backupGateway and an AuditLogger deliberately named gateway. OrderService's single constructor asks for PaymentGateway through parameter gateway. The unrelated same-named logger cannot satisfy the required type. In this actual exercised path, the factory discovers the two compatible PaymentGateway beans, evaluates eligibility and excludes backupGateway because autowireCandidate=false. The backup is still registered and explicitly retrievable. The one eligible gateway instance is passed through the constructor; the service retains the same reference, rather than receiving a copied gateway.

The tracing bean factory observes actual Spring decisions and delegates to the framework. Genuine stdout includes compatible candidates: 2, eligible candidates: 1, unrelated ignored: true and gateway same: true. Fresh required-dependency contexts reproduce missing-type and disabled-only failures; the startup exception is UnsatisfiedDependencyException with root NoSuchBeanDefinitionException. Three JUnit tests genuinely pass. Expected negative context warnings appear on stderr.

This is a simplified controlled resolution path. It does not claim Spring always resolves solely by type, solely by name, or through this universal order. The deliberately wrong-type bean named gateway avoids the straightforward matching-name shortcut here. Spring 6.2's implementation also contains dependency-name/qualifier shortcuts and selection rules; qualifiers, primary status and other cases can matter. No qualifiers/primary test is implied by mentioning that scope. The video concerns Spring-managed beans, with no promise of automatic injection into arbitrary objects created with new.

The recap visibly connects register(SuccessConfig.class) and refresh() to the bean factory's PaymentGateway request, two-compatible/one-eligible result and OrderService(gateway) holding the same managed reference. The graph finishes before the dedicated reading interval. The lesson demonstrates wiring, not a real payment, standalone application/main execution, application-method call or benchmark.

## Final audio-linked animation anchors

| Edit cue | Absolute time |
| --- | --- |
| required.parameter | 3.700000s |
| required.descriptor | 5.020000s |
| discovery.types | 8.240000s |
| discovery.unrelated | 9.820000s |
| discovery.eligibility | 13.540000s |
| selection.unique | 15.140000s |
| selection.supply | 17.480000s |
| selection.stored | 19.480000s |
| missing.no_candidate | 20.880000s |
| missing.failure | 23.660000s |
| recap.verify | 26.220000s |
| recap.scope | 27.720000s |
| recap.match | 31.960000s |
| recap.filter | 32.240000s |
| recap.inject | 32.720000s |
| recap.complete | 33.090000s |

The complete recap remains visible **33.677208–35.677208 seconds**, exactly 2 seconds, before Thanks starts at 35.677208 seconds. Anchors follow final known-input/ASR speech spans; reference-storage and recap-completion delays are explanatory edit choices, not Spring runtime measurements. The 19.480000-second ready-service diagram is not an application-method invocation.

## Captions and encoded-image QA

There are 18 final cues, each 3–7 words, maximum 40 characters, drawn at 52px Inter weight 700. Use white text, centered near X540/Y1380, on a text-width-following rounded black panel at 82% opacity (RGBA alpha 209). Padding is 26px horizontal / 14px vertical; corner radius 12px; maximum padded width 840px; maximum two lines. Measure actual glyph bounds with Pillow textbbox and alpha-composite the RGBA panel. The dedicated caption region is X90..990 / Y1295..1505; every panel remains within the overall safe area X90..990 / Y250..1520. Wrap coherent phrases instead of shrinking typography. No karaoke, bouncing, flashing or distracting caption transitions.

Timing uses exact synthesis sample edges and intermediate unprompted local-ASR word spans, not evenly divided phrases. Caption-only PaymentGateway and An/and mappings retain raw recognition, timestamps and the actual 3.8961039% raw WER. They cannot establish audible pronunciation correctness. Full naturalness, pronunciation and perceived-age acceptance remain unverified without actual listening.

Check source frame-zero equality with cover.png before compression, then inspect actual decoded first-frame.png and opening 0.5/1/2-second samples using suitable image similarity and visual review. Check first-second headline stability, technical motion, continuous transition, caption/diagram separation, small-feed readability and likely 1:1 / 3:4 profile crops. These previews cannot guarantee a platform's crop or automatic thumbnail choice. Geometry, font axes and settings are retained in thumbnail-style.json, subtitle-style.json and font provenance. Actual encoded results and any limitations belong in verification-report.md. Do not claim physical-phone playback, browser playback or auditory acceptance without genuine review. Manual cover and AI-label checks remain in platform-policy-review.md and both platform metadata files.
