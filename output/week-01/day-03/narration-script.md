# Bean registration — narration script

Original English narration for the approved Bean registration lesson. Java annotation names are displayed as @Bean and @Component while spoken as “bean” and “component.” The literal synthesis inputs and phoneme evidence are retained in source/voice/.

The original hook “Why isn't this Java class a Spring bean?” is shortened only for spoken pacing to **“Why isn't this a Spring bean?”** The plain Java Client class and missing Spring registration are visible from frame one. The generated hook utterance lasts1.486333s; no greeting, title-card hold, logo intro or fade delays it.

## Spoken script

Why isn't this a Spring bean?

A class on the classpath isn't automatically registered. Give Spring a registration path.

Register configuration with a bean method. Spring calls the factory and manages its result.

Or add the component annotation, then scan the package containing your class.

Miss that package, and even an annotated class stays unregistered.

Our tests retrieve both. Two paths, one result: Spring knows which beans to manage.

Thanks for watching.

## Timed delivery

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.486333 | Why isn't this a Spring bean? |
| 1.606333–8.786292 | A class on the classpath isn't automatically registered. Give Spring a registration path. |
| 8.966292–16.751125 | Register configuration with a bean method. Spring calls the factory and manages its result. |
| 16.931125–22.585917 | Or add the component annotation, then scan the package containing your class. |
| 22.765917–27.821333 | Miss that package, and even an annotated class stays unregistered. |
| 28.001333–34.679125 | Our tests retrieve both. Two paths, one result: Spring knows which beans to manage. |
| 36.679125–38.037208 | Thanks for watching. |

Source narration lasts **38.387208s**; picture rounds up to **38.400000s** at60FPS (2304frames). The hook uses model inference1.00, the other six coherent utterances0.80. No waveform stretching or pitch shifting is used. The complete overview holds **34.679125–36.679125s**, exactly2s, before the separate spoken Thanks card.

## Technical scope and actual verification

The first lookup occurs in a refreshed context without Client registration and produces the expected NoSuchBeanDefinitionException. A class merely existing on the classpath does not become a managed bean by that fact alone.

The two successful examples use separate contexts. One registers FactoryConfig, whose @Bean method contributes factory metadata during refresh before Spring calls the method and manages its returned Client. The other registers ScanConfig, whose configured @ComponentScan("lesson.scan") discovers @Component Worker before creating its singleton. The annotated Outside class is in lesson.outside and is excluded from that configured scan.

Both illustrated paths create bean definitions before their instances, and both examples use default non-lazy singletons. These are two valid registration paths, not an exhaustive list of every Spring registration API or a claim that all scopes initialize at the same time. The definition registry shown contains selected application beans rather than all internal infrastructure registrations.

Actual Java evidence records **3 JUnit tests passed,0failed**, with compiler, JUnit and standalone execution exit0 and empty stderr. Real proof lines include `plain class missing: true`, `@Bean retrieved: true`, `scan retrieved: true` and `outside scan missing: true`. No code output or test result was invented for the narration. Official Spring documentation and actual runtime evidence remain under source/evidence/java-*.

## Voice acceptance status

The local licensed male Kokoro blend is80%am_puck/20%am_fenrir. Raw unprompted full-stream ASR measures72expected/73recognized words, edit distance2, normalized WER0.027778 (2.7778%). Its discrepancy is the transcription spacing of “classpath” versus “class path”; raw text and scores remain untouched. Alignment provenance documents formatting/word-span normalization separately.

No auditory approval is claimed. Perceived younger-to-middle adult male age, smooth human naturalness, subtle synthesis artifacts and final pronunciation acceptance remain incomplete because this runtime cannot ingest audio for listening review. Objective ASR/signal measurements do not establish those qualities.
