# Bean registration — timed storyboard

This corrected edition responds to the user's report of slow, delayed narration. All speech now uses model inference1.02 with0.08s external joins. The expanded explanation preserves a normal speaking pace; duration is not padded by slowing the model. Source narration is **39.230750s**, rounding to **39.233333s/2354frames at60FPS**. Actual encoded checks are recorded separately.

The palette remains navy/white, cyan requests, purple metadata/components, Spring-green success and red missing registrations. Important content stays inside X=90..990,Y=250..1520. The cover is a separate PNG; the actual video begins with the moving technical hook and immediate narration. Public media contain no week/day/episode numbering.

| Time in seconds | Narration | Progressive mechanism and purpose |
| --- | --- | --- |
| 0.000000–1.541500 | “Why isn't this a Spring bean?” | Frame one shows the plain Client class, a missing Client definition and an application lookup. A request token moves immediately; the class stays outside the managed registry. The separate cover is not held in the video. |
| 1.541500–7.252250 | “The class compiles, but the context has no registration for it. Asking for Client fails.” | Show the unregistered definition slot. Send the teaching lookup at1.661500s and reveal its expected NoSuchBeanDefinitionException at1.961500s, only0.30s later. The failure no longer waits several seconds after the request. |
| 7.252250–13.375667 | “Register FactoryConfig, then refresh. Its @Bean method returns the Client that Spring manages.” | Show ctx.register(FactoryConfig.class) and ctx.refresh(). Reveal the factory definition at9.940s on the spoken bean-method explanation, factory invocation at10.580s on returns, and Client at11.260s when Client is named. Retrieve it at12.275667s; FOUND remains visible before the next scene. Metadata precedes execution and instance creation. |
| 13.375667–20.667292 | “Or add the @Component annotation to Worker, then configure a scan of its package. Spring discovers and registers it.” | Show ScanConfig's activated @ComponentScan("lesson.scan") and the annotated Worker. Scan begins at16.600s; its definition appears at16.720s, Worker at17.000s, and lookup at19.417292s. Hold the successful lookup long enough to read. |
| 20.667292–27.063000 | “The scan covers lesson.scan. Outside lives in another package, so its annotation isn't picked up.” | Name the actual configured package lesson.scan. Bring Outside into view at23.020s and show its missing definition at23.320s,0.30s later. Its @Component annotation does not make an excluded package part of the scan. |
| 27.063000–37.890000 | “Our three tests pass: both registered beans are found; the class outside the scan stays missing. Registration tells Spring what to manage.” | Reveal the retained genuine proof lines @Bean retrieved:true at29.740s, scan retrieved:true at30.540s and outside scan missing:true at32.100s. Assemble registered configuration/refresh → @Bean metadata OR configured component scan → definitions → managed beans/getBean. The graph is complete by35.190s; hold it unchanged from35.890000 to37.890000s for reading. |
| 37.890000–39.230750 | “Thanks for watching.” | Show a separate Thanks for watching card with matching speech and one short cyan underline. The card supplies its own burned words; the SRT retains the closing cue. Preserve the quiet final tail. |

## Captions and sound

- **23 synchronized display cues**, maximum37characters, follow the final96-word narration and documented code-name formatting.
- Seven coherent Kokoro utterances use the licensed80%am_puck/20%am_fenrir male blend at1.02. No waveform stretching or pitch shifting is used.
- Original NumPy music and registration cues are mixed beneath speech with smooth ducking and scene continuity. The audio source retains the exact final effect anchors.
- The complete recap hold is **35.890000–37.890000s**, exactly2s before the separate Thanks scene. This intentional reading pause is retained from the user's format requirements.

## Accuracy and review scope

Both positive cases use separate contexts and default non-lazy singletons. The illustrated registry is limited to the demo beans. Configuration and scan activation precede definitions, factory execution/constructors and later lookup. The annotated Outside class remains excluded from the configured package.

The unchanged Java example's prior genuine3/3test result and stdout remain valid through source-hash comparison; this editorial revision does not claim a fresh Java run. Animation anchors are explanatory edits rather than Spring runtime benchmarks.

The previous file's audio actually started near0.015s, so the perceived delay came from slow0.80 delivery, stacked quiet joins and late visual reveals. This edition addresses those causes. The production agent cannot perform an auditory review; new voice naturalness, pronunciation and perceived age remain unverified. Final encoded opening/transition/closing, mobile readability, caption bounds and audio continuity are owned by the parent verification report.

Approved publication metadata remains **2026-11-18**, proposed **19:00 Asia/Phnom_Penh**. No upload, scheduling or publication is performed.
