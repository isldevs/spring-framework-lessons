# Bean registration — narration script

Original English narration for the approved Bean registration lesson. The user reported that the previous narration felt slow and delayed. This revision uses normal model inference **1.02 for every scene**, shorter **0.08s scene joins**, and more useful explanation rather than slowing a short script to fill the target duration. The male Kokoro style blend remains unchanged.

The opening question is **“Why isn't this a Spring bean?”** The first frame shows the plain Java Client class and its missing Spring registration. The generated hook utterance lasts **1.461500s**; no greeting, static cover hold, logo intro or fade delays it.

## Spoken script

Why isn't this a Spring bean?

The class compiles, but the context has no registration for it. Asking for Client fails.

Register FactoryConfig, then refresh. Its @Bean method returns the Client that Spring manages.

Or add the @Component annotation to Worker, then configure a scan of its package. Spring discovers and registers it.

The scan covers lesson.scan. Outside lives in another package, so its annotation isn't picked up.

Our three tests pass: both registered beans are found; the class outside the scan stays missing. Registration tells Spring what to manage.

Thanks for watching.

## Timed delivery

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.461500 | Why isn't this a Spring bean? |
| 1.541500–7.172250 | The class compiles, but the context has no registration for it. Asking for Client fails. |
| 7.252250–13.295667 | Register FactoryConfig, then refresh. Its @Bean method returns the Client that Spring manages. |
| 13.375667–20.587292 | Or add the @Component annotation to Worker, then configure a scan of its package. Spring discovers and registers it. |
| 20.667292–26.983000 | The scan covers lesson.scan. Outside lives in another package, so its annotation isn't picked up. |
| 27.063000–35.890000 | Our three tests pass: both registered beans are found; the class outside the scan stays missing. Registration tells Spring what to manage. |
| 37.890000–38.980750 | Thanks for watching. |

Source narration lasts **39.230750s**. Picture rounds up to **39.233333s at60FPS (2354frames)**; actual encoded measurements belong in verification-report.md. All seven scenes use one coherent inference batch. No waveform time stretching, pitch shifting or clause-level voice splicing is used. The complete overview holds **35.890000–37.890000s**, exactly2s, before the separate spoken Thanks card.

The literal synthesis inputs contain **96 normalized words**. Public code names are displayed as @Bean, @Component, FactoryConfig and lesson.scan; they are spoken naturally as bean, component, Factory Config and lesson dot scan. Alignment preserves the actual recognized spans and documents those formatting changes.

## Technical scope and retained verification

The first missing lookup is performed after the context is refreshed and throws the expected NoSuchBeanDefinitionException. A compiled class on the classpath is not registered merely by being present.

The two successful examples use separate contexts. Registered FactoryConfig contributes an @Bean factory definition during refresh before the method is called and its Client result is managed. Registered ScanConfig activates @ComponentScan("lesson.scan"), which discovers Worker. The annotated Outside class lives in lesson.outside and stays outside that configured scan. Both examples use default non-lazy singletons and do not exhaust Spring's registration APIs.

The Java sources are unchanged in this pacing revision. The retained genuine run has **3 successful JUnit tests,0failed**, both compilations/standalone execution exit0 and empty stderr. The media verification checks the current source hashes against those tested sources; no new Java execution is claimed. Real proof includes plain class missing:true, @Bean retrieved:true, scan retrieved:true and outside scan missing:true.

## Voice acceptance status

Local licensed Kokoro uses80%am_puck/20%am_fenrir. Fresh unprompted full-stream ASR recognizes **96/96 normalized words**, edit distance0, WER0.000000. Raw recognition and alignment provenance are retained. This objective result does not replace listening.

The user rejected the previous0.80-body pacing. No auditory approval of this corrected version is claimed by the production agent: human naturalness, final pronunciation, subtle artifacts and perceived younger-to-middle adult male age remain unverified because the runtime cannot ingest audio for listening review.
