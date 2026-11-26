# Narration script — Constructor injection

Approved topic: Constructor injection. Publication date2026-11-23, proposed19:00Asia/Phnom_Penh. Internal curriculum numbering is not spoken or shown publicly.

## Spoken script

No Autowired? This still works.

This Spring-managed service has one constructor. Spring selects it automatically. Autowired is optional here.

Spring reads its parameter type: PaymentGateway. In our context, one matching bean is available.

Spring supplies that instance through the constructor. The service keeps the reference.

Now an order calls the injected gateway. Our test checks the same instance and the returned result.

Creating an object with new still means supplying arguments yourself. Let Spring wire the beans it manages.

Thanks for watching.

## Actual narration edit

Local Kokoro v1.0 male80%am_puck/20%am_fenrir blend, inference1.02 for coherent scene utterances. Source duration **36.261917s**,48kHz monoPCM24. Source-derived60FPS ceiling is **2176frames/36.266667s**; final encoded FFprobe values remain authoritative. The mandatory hook is the exact opening phrase,0–1.755125s, with narration starting immediately.

The root-approved addition “Spring selects it automatically.” explains why the annotation can be omitted; the complete second scene is regenerated coherently. No slowdown, artificial pitch shift or individual-word splice is used to fill runtime.

There are20final display cues, maximum41characters. Caption line wrapping uses the new52pxInterBold/max840px measured-panel specification, not the older fixed-width caption style. Primary unprompted ASR has83normalized expected/86observed words,6edits, rawWER7.2289%. The literal script has82whitespace tokens; normalized recognition tokenization differs for compounds/hyphens. Raw recognition and any caption-only glossary/span mappings remain separately retained. No zero-error or listening acceptance is inferred.

## Exact scene/sample boundaries

| Scene edit | Start–end including following edit pause | Spoken phrase |
| --- | --- | --- |
| 1 | 0.000000–1.835125s | No Autowired? This still works. |
| 2 | 1.835125–8.671500s | This Spring-managed service has one constructor. Spring selects it automatically. Autowired is optional here. |
| 3 | 8.671500–14.807000s | Spring reads its parameter type: PaymentGateway. In our context, one matching bean is available. |
| 4 | 14.807000–19.513125s | Spring supplies that instance through the constructor. The service keeps the reference. |
| 5 | 19.513125–25.786708s | Now an order calls the injected gateway. Our test checks the same instance and the returned result. |
| 6 | 25.786708–34.921167s | Creating an object with new still means supplying arguments yourself. Let Spring wire the beans it manages. |
| 7 | 34.921167–36.261917s | Thanks for watching. |

The complete overview reading hold is **32.921167–34.921167s**, exactly2s before the separate spoken Thanks. Ordinary scene joins are0.08s; the ending includes the recorded short tail. These are production edit times, not Spring runtime measurements.

## Thumbnail/caption opening

The entire cover composition is present in source frame0. Its three headline lines are “Spring Injection”, “No @Autowired?” and “It still works.” The headline is not the exact spoken hook, so a separate full-hook caption remains in the dedicated lower caption region. Actual headline sizes are104/96/104px at Inter weight900, with the highlighted line reduced to fit the safe width; captions use52pxInter weight700. The actual glyph union isX110..929/Y499..879; the blue rectangle also remains inside the safe area. The first second preserves the headline while technical background motion begins;1–2s moves the highlighted constructor/code into the explanation. Lossy decoded frames are compared by similarity and visual review, not called pixel-identical to the PNG.

## Technical scope and acceptance

Actual2/2JUnit tests verify a single unannotated constructor on a Spring-managed OrderService, one PaymentGateway candidate, the exact injected reference, the demo execution result and manual construction with caller-provided arguments. The gateway is an in-memory demo; no real payment, standalone application execution or comprehensive behavior test is claimed.

The target voice is a smooth young-to-middle adult male explanation. Actual human naturalness, pronunciation, rhythm, pauses and perceived age require listening acceptance. Automated ASR, G2P and signal checks cannot replace it; no unsupported auditory review is claimed. Publication remains subject to manual approval.
