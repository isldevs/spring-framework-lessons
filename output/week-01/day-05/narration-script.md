# Bean naming — narration script

Original English narration aligned with the final licensed local Kokoro audio. The requested hook “Two bean names can change what Spring finds” is refined for accuracy and pacing to **“Two names. One ambiguous type.”** It starts immediately; the generated hook utterance is1.787625s, and independent recognition places its final word by1.40s. The opening shows actual named-bean/type-selection roles rather than a static title card.

## Spoken script

Two names. One ambiguous type.

This factory method registers a Client named alpha. The annotation supplies its explicit bean name.

Ask for alpha by name, and Spring returns that bean. Add the type argument to check its type too.

With just one Client, a type-only lookup returns the same object. Now register beta as a second Client.

Both beans have clear names, but both match Client. With no primary selected, this type-only lookup is ambiguous.

Our tests verify named results and type failure. Names identify beans; they don't resolve this type tie.

Thanks for watching.

## Sample-derived utterance timing

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.787625 | Two names. One ambiguous type. |
| 1.867625–8.208250 | This factory method registers a Client named alpha. The annotation supplies its explicit bean name. |
| 8.288250–14.389875 | Ask for alpha by name, and Spring returns that bean. Add the type argument to check its type too. |
| 14.469875–21.633917 | With just one Client, a type-only lookup returns the same object. Now register beta as a second Client. |
| 21.713917–28.953042 | Both beans have clear names, but both match Client. With no primary selected, this type-only lookup is ambiguous. |
| 29.033042–35.945417 | Our tests verify named results and type failure. Names identify beans; they don't resolve this type tie. |
| 37.945417–39.036167 | Thanks for watching. |

Source narration is **39.286167s**, rounded up to **39.300000s /2358frames** at60FPS. All seven coherent batches use model inference1.02; ordinary scene joins are0.08s. There is no waveform stretching or pitch shifting. The complete recap reading hold is **35.945417–37.945417s**, exactly2s before the separate spoken Thanks card and final0.25s tail.

## Technical scope

The annotation explicitly names the bean alpha while its Java factory method is client. getBean("alpha") selects by name; getBean("alpha", Client.class) additionally checks that selected bean's type. The single-Client context's type-only lookup returns the same object. A fresh context containing alpha and beta has two different Client instances. Neither is primary and no other selection preference is provided, so this example's getBean(Client.class) fails with NoUniqueBeanDefinitionException.

Names identify beans, while type queries consider matching candidates and applicable selection policies. The script's “this type tie” is scoped to the demonstrated context. It does not claim every multi-candidate query must fail: @Primary and other policies can affect selection. Named lookup is not a @Qualifier annotation. The separate tested qualifier-injection case chooses beta for an injected constructor argument while the direct type-only lookup remains ambiguous.

Actual Java verification records4passing JUnit tests,0failures, and main/test compilation plus standalone execution exit0 with empty stderr. The printed proofs and exception are retained under source/evidence/java-*. No test result or code output is invented for narration.

## Voice-review limit

Local80%am_puck/20%am_fenrir male English styles are used with model/license/hash evidence. Fresh unprompted full-stream ASR recognizes97/97normalized words with edit distance0 and WER0. Raw ASR and actual signal/pause metrics are retained; typography/case and Java spelling formatting are documented separately.

No auditory listening approval is claimed. Human naturalness, pronunciation acceptance, perceived younger-to-middle adult age and subtle synthesis artifacts remain unverified because this runtime cannot ingest the audio for listening review. Those objective results do not complete subjective voice acceptance.
