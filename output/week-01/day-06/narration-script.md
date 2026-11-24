# Multiple contexts — narration script

Original English narration for the approved Multiple contexts lesson. The supplied hook “Can two Spring contexts see different beans?” is shortened for spoken pacing to **“Two contexts. Different beans?”** The source hook utterance lasts 1.705292 seconds and begins immediately. Independent final recognition places its last word by 1.36 seconds. The video opens on two concrete context registries and their different lookup results; there is no static cover hold or greeting.

## Spoken script

Two contexts. Different beans?

Yes. Register alpha in context A, and beta in B. Each independent context has its own registry.

Context A finds alpha, but beta is missing. Sharing one Java application doesn't connect these registries.

Create a fresh parent and child. Set the parent before refreshing the child. The registries stay separate.

The child checks locally first. A missing named bean can be found in its parent.

The parent cannot search its children. Our tests confirm both directions: child to parent works; parent to child doesn't.

Thanks for watching.

## Sample-derived utterance timing

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.705292 | Two contexts. Different beans? |
| 1.785292–8.818042 | Yes. Register alpha in context A, and beta in B. Each independent context has its own registry. |
| 8.898042–16.071458 | Context A finds alpha, but beta is missing. Sharing one Java application doesn't connect these registries. |
| 16.151458–22.310583 | Create a fresh parent and child. Set the parent before refreshing the child. The registries stay separate. |
| 22.390583–27.147417 | The child checks locally first. A missing named bean can be found in its parent. |
| 27.227417–34.771750 | The parent cannot search its children. Our tests confirm both directions: child to parent works; parent to child doesn't. |
| 36.771750–37.862500 | Thanks for watching. |

Source narration lasts **38.112500 seconds**, rounded up to **38.116667 seconds / 2287 frames** at 60 FPS for the planned picture. Actual encoded metadata is recorded in verification-report.md. All seven coherent scene batches use normal model inference speed 1.02. The leading context label A is supplied as its letter pronunciation /eɪ/ in the corrected third coherent batch; the spoken text remains “Context A finds alpha”. Ordinary joins are 0.08 seconds; there is no waveform stretching or pitch shifting.

The complete overview reading hold is **34.771750–36.771750 seconds**, exactly two seconds after the mechanism explanation and before the separate spoken Thanks card. The final source quiet tail is 0.25 seconds.

## Technical scope and actual verification

The demonstrations use named `getBean` lookup. Independent contexts A and B are initialized from different configurations, registering demo beans alpha and beta respectively. A named lookup in A does not search independent B, and the reverse lookup also fails. Both contexts remain initialized; this is a lookup visibility result rather than a startup failure.

The parent-child demonstration creates a fresh parent and child. `child.setParent(parent)` runs before the child registers its configuration and calls `refresh()`. The child checks its own factory first; when the requested name has no local bean, lookup can fall back to the parent. `child.getBean("shared", Item.class)` returns the same managed instance as the parent's lookup. The bean is not copied into the child's local registry: `child.containsLocalBean("shared")` is false. The parent's lookup for the child's local bean fails because normal parent lookup does not search child contexts.

A separate test verifies that a child's local bean with the same name hides the parent's named bean for child lookup. Bean-listing APIs have their own hierarchy rules; this narration does not generalize named lookup to every container API. Diagram entries show selected application beans and omit Spring infrastructure beans.

Actual Java verification records **four passing JUnit tests and zero failures**. Main/test compilation, JUnit execution and the standalone ContextsDemo all exit successfully with empty stderr. Complete commands, outputs, exceptions, source hashes and official documentation evidence remain under source/evidence/java-*. No narration proof line is fabricated.

## Voice-review limit

Local licensed male English Kokoro styles use an 80% am_puck / 20% am_fenrir blend. Model/license/hash evidence, coherent scene segments, pronunciation phonemes, independent ASR and signal/pause measurements are retained under source/voice/.

Final unprompted small.en ASR returns 91 words against 91 expected words, with two substitutions and a normalized word error rate of 2.1978%. The recognizer writes “registry stays” for the script’s “registries stay”. The caption-only alignment maps those two observed word spans to the intended script words, with explicit provenance; the raw transcript and score remain unchanged. There are 22 synchronized SRT cues, at most 34 characters each. These are recognition/alignment results, not proof of perceptual voice quality.

No auditory listening approval is claimed. Human naturalness, pronunciation acceptance, perceived younger-to-middle adult age and subtle synthesis artifacts remain unverified because no supported listening review is available. Automated recognition and signal checks do not complete that perceptual acceptance requirement.
