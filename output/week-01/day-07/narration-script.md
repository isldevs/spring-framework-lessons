# Context smoke test — narration script

Original English narration for the approved Context smoke test lesson. The supplied hook “Your app starts, but did Spring wire it?” is refined for pacing and precise scope to **“Context loaded. Wiring checked?”** The hook asks whether expected wiring was tested without implying that context readiness proves comprehensive application correctness. Its actual utterance ends at 1.837792s. Narration begins immediately over a concrete ready-context/pending-assertion visual; the separate cover does not delay the hook.

## Spoken script

Context loaded. Wiring checked?

Spring's JUnit support loads our configuration before the test. It creates a repository and supplies it to our service.

Retrieve the required service bean from the context.

Compare its repository with the context's repository. Assert they're the same object. Matching values aren't enough.

Run the smoke test. It passes: context loaded, required bean found, expected dependency confirmed.

This checks wiring for our configuration. Test order behavior separately. Load, look up, assert.

Thanks for watching.

## Sample-derived utterance timing

| Time in seconds | Spoken phrase |
| --- | --- |
| 0.000000–1.837792 | Context loaded. Wiring checked? |
| 1.917792–10.014000 | Spring's JUnit support loads our configuration before the test. It creates a repository and supplies it to our service. |
| 10.094000–12.927333 | Retrieve the required service bean from the context. |
| 13.007333–20.531958 | Compare its repository with the context's repository. Assert they're the same object. Matching values aren't enough. |
| 20.611958–27.449125 | Run the smoke test. It passes: context loaded, required bean found, expected dependency confirmed. |
| 27.529125–33.644792 | This checks wiring for our configuration. Test order behavior separately. Load, look up, assert. |
| 35.644792–36.735542 | Thanks for watching. |

Actual source narration lasts **36.985542 seconds**, giving a frame-rounded planned picture of **37.000000 seconds / 2220 frames** at 60 FPS. Actual encoded metadata is measured separately in verification-report.md. All seven coherent scene batches use normal model inference speed 1.02, with 0.08s ordinary joins, no waveform stretching and no pitch shifting. The required-bean and closing-scope sentences were shortened to preserve normal pacing while reaching the requested runtime; those scenes were regenerated as whole utterances.

The complete overview reading hold is **33.644792–35.644792 seconds**, exactly 2 seconds after the mechanism narration and before separate spoken Thanks. Source closing includes a 0.25s quiet tail.

## Technical scope and actual verification

The test uses `@SpringJUnitConfig(Config.class)` and an `@Autowired ApplicationContext`. JUnit owns the test fixture; Spring's test support loads the selected configuration and injects access to that context. The illustration does not claim a newly created context for every test method or a specific ApplicationContext implementation.

Config's default singleton demo beans are Repo and OrderService. Spring supplies Repo through the OrderService factory method/constructor before the test retrieves the service. The test calls `getBean(OrderService.class)` and `getBean(Repo.class)`, asserts both are non-null, and uses `assertSame(repo, service.repository())` to check the expected reference identity. Equal values alone do not establish that relationship. Other scopes or designs can require different assertions.

Actual verification records **one JUnit test passed, zero failures or skips**. Main/test compilation and JUnit execution exit 0 with empty stderr. No standalone application execution is claimed. The actual test prints `bean found: true` and `wiring same: true` only after the real assertions pass. Full commands, JUnit XML, raw output, source hashes and official documentation evidence remain under source/evidence/java-*.

This smoke test covers the selected configuration and assertions. It does not prove order behavior, database operations, other configurations, all lazy beans or every application feature. Separate behavior tests remain necessary. `@DirtiesContext(AFTER_CLASS)` is used for deliberate demo cleanup rather than claimed as universally required.

## Captions and voice-review limit

There are 20 synchronized SRT cues, maximum 34 characters. Captions follow final scene/sample boundaries and independent word timing.

Final raw unprompted faster-whisper small.en int8 records 78 expected words, 78 observed words, edit distance 6 and raw word error rate 7.6923%. These are recognition metrics, not proof of human voice naturalness. Four explicit caption-only transformations relabel two observed being spans as the known synthesis word bean, merge they/are spans for the scripted contraction, and share the observed lookup span across look/up. No within-word boundary is invented, and the raw transcript and score remain unchanged. A separate bounded base.en recognition trial records3edits/3.8462% and is not substituted for the primary result.

Local licensed male English Kokoro styles use an 80% am_puck / 20% am_fenrir blend. Model/style hashes, licenses, coherent segments, pronunciation phonemes and signal/pause evidence are retained under source/voice/. No actual listening approval is claimed. Smooth human explanation, pronunciation acceptance, perceived younger-to-middle adult age and subtle synthesis artifacts remain unverified by automated recognition, pitch, silence or clipping measurements.
