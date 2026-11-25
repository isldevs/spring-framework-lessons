# Context smoke test — timed storyboard

Seven scenes follow final locally generated Kokoro speech. Times below are sample-derived edit boundaries; visible changes land on the applicable 60 FPS frame. Source narration is **36.985542 seconds**; planned picture ceiling is **37.000000 seconds / 2220 frames**. Measured encoded values belong in verification-report.md.

Dark navy, white text, cyan requests, purple configuration/components and Spring green managed instances/success distinguish the mechanism. Important content stays inside X=90..990 / Y=250..1520; captions reserve a separate lower band. Diagrams show selected application beans and omit Spring infrastructure beans. JUnit's test fixture is not drawn as a managed application bean. These are illustrative editing times, not runtime measurements.

| Time | Narration | Progressive mechanism and audience purpose |
| --- | --- | --- |
| 0.000000–1.917792 | Context loaded. Wiring checked? | A ready context and an unresolved expected-reference assertion are visible from frame one. A purposeful request/reference pulse moves immediately while the spoken hook asks whether wiring has been checked. There is no cover/title hold, black frame, greeting, fade or logo intro; the branded cover PNG is separate. |
| 1.917792–10.094000 | Spring's JUnit support loads our configuration before the test. It creates a repository and supplies it to our service. | Outside the context, show JUnit invoking Spring test support through @SpringJUnitConfig(Config.class). Follow the selected configuration into the context: @Bean Repo is created, its reference is supplied to @Bean OrderService service(Repo repo), and the constructor relationship is assembled before the ready marker. Keep the JUnit-owned test fixture outside the managed application-bean graph. |
| 10.094000–13.007333 | Retrieve the required service bean from the context. | Animate the test calling ctx.getBean(OrderService.class). Locate the selected managed service and return its reference to the test. The existing default singleton remains in the context; the lookup does not rerun its factory in this demo. |
| 13.007333–20.611958 | Compare its repository with the context's repository. Assert they're the same object. Matching values aren't enough. | Retrieve the expected Repo reference from the context. Follow service.repository() to the same Repo object and compare the two references with assertSame. Reveal object identity, rather than a values-only comparison or a duplicated repository object. |
| 20.611958–27.529125 | Run the smoke test. It passes: context loaded, required bean found, expected dependency confirmed. | Reveal the real JUnit smoke test's successful result after the already-shown assertions: bean found: true and wiring same: true. Display the measured one-test passing result without implying untested application behavior has passed. |
| 27.529125–35.644792 | This checks wiring for our configuration. Test order behavior separately. Load, look up, assert. | Assemble the complete overview from JUnit/Spring support through Config, managed beans and constructor wiring, required lookup and reference assertion to pass. Keep the selected-configuration scope visible. Grey order-behavior tests remain a separate task, not a fabricated failure. Hold the completed diagram for exactly two seconds before Thanks. |
| 35.644792–36.985542 | Thanks for watching. | Cut to the separate Thanks for watching card with its brief purposeful accent reveal. Preserve its words through the final source quiet tail and frame-rounded picture end; avoid duplicate burned captions over the card. |

## Reading hold, captions and pacing

The complete recap holds **33.644792–35.644792 seconds**, exactly 2 seconds, before the separate Thanks scene begins at 35.644792 seconds. Do not count the end card as the diagram's reading hold.

There are 20 synchronized SRT cues, maximum 34 characters. Captions follow final scene/sample boundaries and independent word timing. All utterances use normal inference speed 1.02 with 0.08s ordinary joins. There is no waveform stretching, pitch shifting or slowing to fill runtime. Original NumPy music and meaningful event sounds stay beneath narration.

## Narration-synchronized mechanism anchors

These are actual edit cues from source/timing.json and the renderer, not measurements of Spring/JUnit runtime performance.

| Seconds | Visible cue |
| --- | --- |
| 4.060000 | Spring/JUnit configuration and bean creation — configuration |
| 6.800000 | Spring/JUnit configuration and bean creation — repo |
| 7.900000 | Spring/JUnit configuration and bean creation — injection |
| 9.470000 | Spring/JUnit configuration and bean creation — ready |
| 10.094000 | Required service lookup — request |
| 11.590000 | Required service lookup — return |
| 13.600000 | Repository reference identity assertion — actual |
| 15.580000 | Repository reference identity assertion — expected |
| 16.820000 | Repository reference identity assertion — assertion |
| 18.360000 | Repository reference identity assertion — pass |
| 20.611958 | Actual test proof — result |
| 22.060000 | Actual test proof — pass |
| 24.240000 | Actual test proof — bean |
| 25.580000 | Actual test proof — wiring |
| 27.529125 | Completed mechanism and scope overview — scope |
| 30.520000 | Completed mechanism and scope overview — behavior |
| 32.260000 | Completed mechanism and scope overview — load |
| 32.420000 | Completed mechanism and scope overview — lookup |
| 32.640000 | Completed mechanism and scope overview — assert |
| 33.170000 | Completed mechanism and scope overview — complete |
| 33.644792 | Overview — recap hold start |
| 35.644792 | Overview — recap hold end |

The recap load/lookup/assert sequence is a documented illustrative edit. Raw ASR assigns `Load` zero duration at 32.260000s, the same start as its observed `lookup` span. The diagram reveals Load at 32.260000s, lookup at the derived 32.420000s (160ms later) and assert at 32.640000s. This keeps the recap readable without inventing a spoken within-word boundary or changing the raw ASR times. The complete state appears at 33.170000s, before the separate exact two-second reading hold.

## Technical boundaries and genuine proof

Spring test support loads the selected Config. Its Repo and OrderService are default singleton beans, with Repo supplied through the service's constructor. Required type lookup and assertSame confirm the expected selected relationship. The object remains managed by the context while only references return to the test. Equal values alone do not establish identity; different scopes can require other assertions.

Actual Java verification records **one passing JUnit test**, zero failures/skips. Main/test compilation and JUnit execution exit 0 with empty stderr. `bean found: true` and `wiring same: true` are literal test stdout after successful assertions. No standalone application output or comprehensive behavior success is invented. Six official Spring/JUnit documentation responses and actual source hashes/commands/JUnit XML remain under source/evidence/java-*.

The selected configuration and these assertions are the test's scope. Order behavior, database operations and other application features require separate tests. Compatible Spring test contexts can be cached; this demonstration does not promise a fresh context for every test method. The demo's @DirtiesContext(AFTER_CLASS) cleanup is not described as universally required.

Source previews do not certify the final encoded file. Root QA inspects actual opening frames, transitions, captions, audio continuity, recap hold and ending. No auditory approval or physical-phone playback review is inferred from this storyboard.
