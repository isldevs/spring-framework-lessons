# Narration script — Dependency resolution

Approved topic: Dependency resolution. Publication date: 2026-11-24, proposed 19:00 Asia/Phnom_Penh. Internal curriculum numbering is not spoken or shown publicly.

## Spoken script

How does Spring know what to inject?

The order service constructor requests a PaymentGateway. Spring reads that dependency.

The bean factory finds compatible types. An unrelated logger won't match. Matching beans must also be eligible.

Here, one eligible gateway remains. Spring supplies its instance to the constructor.

Without an eligible candidate, this required constructor dependency stops context startup.

Our tests verify both outcomes. Qualifiers and primary settings can also affect selection. Match, filter, inject.

Thanks for watching.

## Actual narration edit

The literal script has 77 whitespace-delimited words. Local Kokoro v1.0 uses a male 80% am_puck / 20% am_fenrir blend at inference speed 1.02 for coherent scene utterances. The actual narration WAV is **37.017958 seconds**, 48kHz mono PCM24. The source-derived 60 FPS ceiling is **2222 frames / 37.033333 seconds**; actual final encoded FFprobe values remain authoritative. The exact opening hook occupies 0–1.604167 seconds, with its synthesis edit starting at zero.

Ordinary joins are 0.08 seconds. The complete overview has a separate **33.677208–35.677208 second reading hold**, exactly 2 seconds before the spoken Thanks. The short tail ends at 37.017958 seconds. No artificial slowdown, pitch shift or isolated-word splicing is used to fill runtime.

There are 18 final display cues, each 3–7 words, at most 40 characters. Primary unprompted local small.en ASR has 77 normalized reference words, 78 observed words and 3 edit operations: raw WER **3.8961039%**. Raw recognition, timestamps and score remain unchanged. Caption-only mapping uses the observed payment/gateway span for the known scripted class name PaymentGateway, and the observed “and” span for the known input “An.” These explicit mappings do not establish pronunciation correctness; their provenance is retained in source/voice/alignment-normalization.json.

Scene edges come from exact synthesis sample edits. Intermediate caption boundaries use actual unprompted ASR word spans rather than evenly divided timing. The full hook remains one cue from zero to the exact utterance end. Derived diagram delays are explanatory edits, not Spring runtime measurements.

## Exact scene/sample boundaries

| Scene edit | Start–end including following edit pause | Spoken phrase |
| --- | --- | --- |
| 1 | 0.000000–1.684167s | How does Spring know what to inject? |
| 2 | 1.684167–6.918542s | The order service constructor requests a PaymentGateway. Spring reads that dependency. |
| 3 | 6.918542–14.664042s | The bean factory finds compatible types. An unrelated logger won't match. Matching beans must also be eligible. |
| 4 | 14.664042–20.001000s | Here, one eligible gateway remains. Spring supplies its instance to the constructor. |
| 5 | 20.001000–25.823083s | Without an eligible candidate, this required constructor dependency stops context startup. |
| 6 | 25.823083–35.677208s | Our tests verify both outcomes. Qualifiers and primary settings can also affect selection. Match, filter, inject. |
| 7 | 35.677208–37.017958s | Thanks for watching. |

## Thumbnail/caption opening

The complete cover composition is present in source frame zero. Its three headline lines are “How Spring”, “Finds Your” and “Dependencies”; only the last line has the rounded blue #0866FF highlight. Actual Inter weight 900 text is 104px on each line. The glyph union is X110..851 / Y499..899; the blue highlight is X110..869 / Y793..907, within the safe area.

Because the headline is not the literal spoken hook, a separate exact full-hook caption uses the dedicated lower caption region. Its two rendered lines are “How does Spring know” / “what to inject?” in 52px Inter weight 700. The first second preserves the readable headline while the constructor's dependency request moves toward the bean factory. From 1–2 seconds, the actual constructor code moves into the explanation. Source/cover equality and decoded-image similarity are distinct checks; lossy decoded frames are not called pixel-identical to the PNG.

## Technical scope and acceptance

Three actual JUnit tests verify the demonstrated full candidate path, exact injected reference and two required-dependency startup failures. SuccessConfig registers two compatible PaymentGateway beans; backupGateway is marked autowireCandidate=false, so it remains registered but is excluded from injection. The AuditLogger named gateway has the wrong type. The observer-only tracing factory delegates to Spring. Missing-type and disabled-only contexts fail with UnsatisfiedDependencyException rooted in NoSuchBeanDefinitionException.

This is a simplified selected path, not a claim that every Spring dependency follows a universal type-first or name-only sequence. Qualifiers, primary settings, name shortcuts and other cases can affect selection. The example concerns Spring-managed beans; arbitrary new-created objects are not promised automatic injection. No real payment, standalone application/main invocation, service business execution or comprehensive behavior test is claimed.

The target is a smooth young-to-middle adult male explanation. Human naturalness, pronunciation, rhythm, joins and perceived age still require actual listening acceptance. ASR, G2P, pitch and signal metrics cannot replace it. **Auditory acceptance remains unverified; production must not be represented as fully complete until that essential gate is satisfied.** Publication requires manual approval.
