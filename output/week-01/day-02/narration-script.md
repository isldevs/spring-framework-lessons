# ApplicationContext — narration script

Original English narration, synchronized to the final local Kokoro audio. The public API names are written ApplicationContext and getBean; they are spoken naturally as “application context” and “get bean.” The generator retains the literal speech inputs and phoneme evidence.

The requested hook “What actually lives inside ApplicationContext?” is shortened only for spoken pacing to **“What's inside ApplicationContext?”** It starts immediately and its generated utterance ends at 1.963s. There is no greeting, title-card hold, logo intro or fade. A concrete definition-versus-object cutaway is visible from frame one.

## Spoken script

What's inside ApplicationContext?

Bean definitions are recipes. Managed instances are the actual objects.

Register configuration, then refresh. Spring reads the definitions and creates our singleton beans.

Calling getBean returns the service, already wired to its repository.

The context also publishes events. Close it, and managed cleanup runs.

Our tests confirm: same service, one event, cleanup called. Definitions describe; instances do the work.

Thanks for watching.

## Timed delivery

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.963000 | What's inside ApplicationContext? |
| 2.083000–7.376042 | Bean definitions are recipes. Managed instances are the actual objects. |
| 7.556042–14.796708 | Register configuration, then refresh. Spring reads the definitions and creates our singleton beans. |
| 14.976708–19.860875 | Calling getBean returns the service, already wired to its repository. |
| 20.040875–24.956250 | The context also publishes events. Close it, and managed cleanup runs. |
| 25.136250–32.275958 | Our tests confirm: same service, one event, cleanup called. Definitions describe; instances do the work. |
| 34.275958–35.462000 | Thanks for watching. |

The literal speech inputs contain 67 normalized words. Source narration lasts **35.812000 s**; the 60FPS picture rounds up to **35.816667 s** (2149 frames). The hook uses model inference speed 1.00; the other six coherent scene utterances use 0.90. No waveform stretching or pitch shifting is applied. A two-second reading hold, **32.275958–34.275958s**, follows the verification/takeaway narration; the separate spoken Thanks card comes afterward.

## Technical scope and evidence

“Definitions” means bean construction metadata, not object instances. The main example registers Config.class in a new, unrefreshed AnnotationConfigApplicationContext, then refreshes. Infrastructure definitions are already present; the diagram illustrates the demo's application beans. Its @Bean method definitions are discovered during configuration processing inside refresh before the corresponding Repo and Service singleton objects are created. ApplicationContext delegates bean definition/instance handling to its bean factory.

The script's “our singleton beans” refers to this non-lazy default-singleton demonstration. A separate real test shows a lazy definition can exist without its instance after refresh. getBean returns the existing wired service in this example. The same context dispatches a DemoEvent to Service's listener and invokes that singleton's DisposableBean cleanup when closed; the narration does not claim every bean scope has identical timing or destruction behavior.

The actual Java evidence records two passing JUnit tests and the exact lines `same service: true`, `events handled: 1` and `cleanup called: true`. No output was invented for narration. Official Spring documentation evidence is retained in source/evidence/java-doc-*.

## Voice acceptance status

Licensed local Kokoro male styles are used in a 80% am_puck / 20% am_fenrir blend. Objective unprompted ASR recognizes all 67 expected normalized words, but ASR is not a listening review. Perceived younger-to-middle adult age, humanlike smoothness, subtle synthesis artifacts and final pronunciation acceptance remain incomplete because this runtime cannot ingest audio for auditory review. Do not represent the audio as auditorily approved.
