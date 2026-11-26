# Constructor injection — reproducible Java/Spring verification

This minimal project runs two real JUnit/Spring tests for a Spring-managed `OrderService` with **one constructor and no `@Autowired` on that constructor**. Spring resolves its one `PaymentGateway` candidate and supplies it to the constructor. The service executes through that gateway. A second test shows a manually created service retaining the gateway supplied by its Java caller.

## Run

Requirements: Java17 or newer and Python3. The captured run used OpenJDK21.0.13, ECJ3.40.0 targetingJava17, Spring Framework/spring-test6.2.11, Micrometer1.15.4, JUnit Jupiter5.12.2/Platform1.12.2. No Maven, javac or Spring Boot execution is claimed.

```sh
bash run.sh
```

Eleven pinned JARs are retained in `lib/`, together with SHA-256 and source-URL manifests. `fetch-dependencies.py` obtains or revalidates them against published Maven Central SHA-1 values and extracts license/notices. `verify.py` checks the manifest, actually compiles main/test sources and runs JUnit. Raw command arrays, working directories, exit codes, stdout/stderr, XML, runtime version and five Java-source hashes are saved in `../evidence/java-*`.

## Actual results

**2/2 tests passed**, zero failed/error/skipped cases. Main compilation, test compilation and JUnit each exited0 with empty stderr. Exact real JUnit stdout emitted after assertions:

```text
constructors: 1
autowired: false
gateway same: true
order result: demo-paid:2500
manual uses caller: true
```

The first test checks the reflection-visible constructor count, its `PaymentGateway` parameter and absence of `@Autowired`; exactly one gateway candidate; required typed bean lookups; exact dependency reference; and the delegated result. The manual control checks the caller's gateway is retained, is not the context's gateway and the manually created service is not the managed singleton.

## Registration and runtime flow

- `Config` uses `@Import({OrderService.class, DemoPaymentGateway.class})` to register the two component classes. This is explicit component registration; no component scan is claimed.
- `OrderService` is annotated `@Service`. Its sole public constructor takes `PaymentGateway` and assigns it to a final field. That constructor has no `@Autowired` annotation.
- `DemoPaymentGateway` is the only registered implementation of `PaymentGateway`; the beans use the default singleton scope. Spring resolves that candidate and creates `OrderService` with that reference.
- Typed lookups use `ctx.getBean(OrderService.class)` and `ctx.getBean(PaymentGateway.class)`. No particular bean name is asserted or required.
- JUnit creates the test fixture. Spring TestContext (`@SpringJUnitConfig`) loads the selected configuration and injects the fixture's context field. The test fixture's `@Autowired ctx` is separate from the deliberately unannotated service constructor.
- The framework owns the context lifecycle. `@DirtiesContext(AFTER_CLASS)` is explicit demo cleanup, not a general recommendation to reload every non-mutating test. Compatible contexts may be cached.

`gateway()` is exposed to make this small identity assertion explicit. `placeOrder(2500)` calls the actual injected collaborator's `charge(2500)`. The collaborator is an **in-memory demonstration**, returning a string. It performs no network call or real payment, and the tests do not establish comprehensive application or financial behavior.

## Documentation and limits

Matching official Spring6.2.11 `Autowired` API documentation states that a class with a single constructor uses it even when unannotated. The Spring6.2 reference documents this support since4.3. Additional official API references verify regular component `@Import` registration, SpringJUnitConfig context loading, bean lookup and JUnit reference-identity assertions. `fetch-docs.py` reproduces the actual HTML/text/hash/claim evidence under `../evidence/java-doc-*`.

The rule applies to Spring-managed beans. Annotating a class as `@Service` does not make an arbitrary `new OrderService(...)` instance receive automatic Spring injection. Java callers still supply constructor arguments. Multiple-constructor or multiple-candidate selection rules are not generalized from this one-constructor/one-candidate example.

All JAR license/notices and ECJ EPL evidence are retained in `licenses/`. No standalone application main, startup benchmark, real payment, browser playback or narration review is claimed by this Java project.
