# Multiple contexts — timed storyboard

Seven scenes follow the final local Kokoro narration and sample-derived edit boundaries in source/timing.json. Times are seconds from video start; changes land on the applicable 60 FPS frame. Source audio is **38.112500 seconds**, with planned picture **38.116667 seconds / 2287 frames**. Actual encoded measurements belong in verification-report.md.

Dark navy, white text, cyan requests, purple definitions/context boundaries, Spring green instances/results and red missing-lookup outcomes distinguish the mechanism. Important text, diagrams and captions stay inside X=90..990 and Y=250..1520. The diagrams show selected application beans rather than every Spring infrastructure definition. These are illustrative editing times, not Spring runtime performance measurements.

| Time | Narration | Progressive mechanism and audience purpose |
| --- | --- | --- |
| 0.000000–1.785292 | Two contexts. Different beans? | A concrete alpha lookup succeeds in context A and fails in independent context B, where beta remains visible. A cyan lookup pulse moves from the opening frame. The question is spoken immediately; there is no cover/title hold, greeting, fade or logo intro. The branded cover PNG is separate. |
| 1.785292–8.898042 | Yes. Register alpha in context A, and beta in B. Each independent context has its own registry. | Reveal application startup for context A: a.register(AConfig.class), then a.refresh(). The alpha definition becomes a managed Item instance in A. On the spoken beta, switch the startup snippet to b.register(BConfig.class), then b.refresh(), creating beta in B. Separate local demo registries preserve ownership throughout. |
| 8.898042–16.151458 | Context A finds alpha, but beta is missing. Sharing one Java application doesn't connect these registries. | Animate a.getBean("alpha") and its local success, then change the requested name to beta. The lookup misses in A while beta stays visible in B. Both contexts remain ready. No cross-context search path is drawn because the independent contexts have no parent relationship. |
| 16.151458–22.390583 | Create a fresh parent and child. Set the parent before refreshing the child. The registries stay separate. | Introduce a fresh parent and child, with ParentConfig/shared and ChildConfig/local. Highlight child.setParent(parent) before child.refresh(). The parent link is established before the child definition becomes its managed local instance. The earlier independent A/B pair is not reconfigured while running. |
| 22.390583–27.227417 | The child checks locally first. A missing named bean can be found in its parent. | Follow child.getBean("shared") into the child local registry. Show that the name is absent locally, then traverse the parent link and locate shared. Return a reference to the same parent-managed Item. The shared instance stays in the parent; no copy or extra child definition appears. |
| 27.227417–36.771750 | The parent cannot search its children. Our tests confirm both directions: child to parent works; parent to child doesn't. | Show parent.getBean("local") missing, with the child local instance still present. Reveal actual proof lines “child shared same: true” and “parent local: missing”. Assemble the completed named-lookup overview: child can fall back upward; parent cannot search downward. Hold the complete diagram for two seconds after the narration and before Thanks. |
| 36.771750–38.112500 | Thanks for watching. | Cut to the separate Thanks for watching card with its brief cyan underline reveal. Its words match the spoken thanks and avoid duplicate burned captions. Preserve the card through the final quiet tail and frame-rounded picture end. |

## Reading hold and captions

The entire completed recap holds **34.771750–36.771750 seconds**, exactly two seconds. The separate Thanks scene begins at **36.771750 seconds**. The diagram hold is completed before the end card, rather than counted as the movie's final two seconds.

There are 22 synchronized SRT cues, maximum 34 characters. Captions follow the final narration and reserve their own lower band. Source/timing.json and the separate subtitles.srt retain exact cue intervals. All speech is synthesized in coherent scene-level batches at normal inference speed 1.02, with 0.08-second ordinary joins and no waveform stretching or pitch shifting. The corrected third phrase pronounces context label A as a letter. Original NumPy music and meaningful lookup sounds are mixed beneath narration.

## Narration-synchronized mechanism anchors

These edit anchors come from source/timing.json and the renderer. They illustrate lookup order and are not measurements of Spring execution speed.

| Time in seconds | Visible mechanism |
| --- | --- |
| 2.660000 / 3.010000 | Reveal alpha's definition, then begin its definition-to-instance transition in context A. |
| 4.560000 / 4.910000 | Switch startup to B, reveal beta's definition, then begin its instance transition in B. |
| 8.898042 / 10.210000 | Start A's named lookup; confirm local alpha. |
| 10.740000 / 11.400000 | Request beta from A; reveal the missing result while B keeps beta. |
| 18.060000 / 19.060000 | Establish the fresh child's parent link, then refresh the child. |
| 23.160000 / 24.460000 | Check the requested shared name locally; show the child-local miss. |
| 26.340000 / 26.540000 | Follow the link to the parent and begin returning the existing parent instance reference. |
| 27.340000 / 28.620000 | Request local through the parent; reveal missing reverse visibility. |
| 29.540000 | Reveal actual Java proof lines for parent-instance identity and missing reverse lookup. |
| 31.900000 / 33.060000 | Reveal upward named fallback and the blocked reverse path in the overview. |
| 34.630000 | Show the completed overview verification check, aligned with its sound cue. |
| 34.771750–36.771750 | Preserve the completed diagram for the two-second reading hold. |

## Technical boundaries and proof

The mechanism is **named getBean lookup**. Independent contexts have separate factories and no parent link. The hierarchy uses fresh contexts, and setParent runs before child refresh. The child checks locally before upward fallback; its parent-owned shared object is not copied locally. The parent cannot automatically search its children for the local bean. A separate test shows that a child's same-name local bean hides the parent for that child's named lookup. Listing/type-enumeration APIs have their own hierarchy rules.

The missing outcomes occur after successful initialization and do not depict startup failure. The application supplies configuration and initiates each lookup. The diagrams retain container boundaries and managed instances while references return to the caller.

Actual Java verification records **four passing JUnit tests and zero failures**, with actual compilation, JUnit and application output retained under source/evidence/java-*. The proof lines are taken from that executed application. Five versioned official Spring API pages support the explanation. Neither this storyboard nor a source-preview contact sheet certifies the final encoded video. Root QA inspects actual opening frames, transitions, captions, audio continuity, recap hold and ending.

Human naturalness, pronunciation and perceived voice age remain incomplete by auditory acceptance; no listening review is claimed.
