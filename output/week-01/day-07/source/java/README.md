# Context smoke test — reproducible Java example

This minimal Spring Framework/JUnit project genuinely loads `Config.class` through `@SpringJUnitConfig`, retrieves the required `OrderService` and `Repo` beans, and checks that the service received the exact repository object from the context. The one smoke test does not exercise ordering rules, database access, HTTP endpoints or full-application behavior.

## Run

Requirements: Java17 or newer and Python3. The recorded run used OpenJDK21.0.13, ECJ3.40.0 targetingJava17, Spring Framework/spring-test6.2.11, Micrometer1.15.4, JUnit Jupiter5.12.2 and Platform1.12.2. Maven and javac are not required or claimed.

```sh
bash run.sh
```

The dependency fetcher uses Maven Central HTTPS, verifies each published SHA-1 and writes a SHA-256 manifest for all11pinned JARs. The verification script checks the SHA-256 manifest, actually compiles main/test sources, executes `ContextSmokeTest` through JUnit, parses the generated XML and checks the exact proof lines. A separate application main is intentionally absent: the required actual execution is the JUnit/Spring TestContext run.

## Actual result

The captured execution passed **1/1JUnit test**, with zero skipped/failed/error cases. Main compilation, test compilation and JUnit exited0 with empty stderr. After all assertions passed, the test emitted:

```text
bean found: true
wiring same: true
```

These are genuine captured lines from `../evidence/java-junit.stdout.txt`. Complete commands, stdout/stderr, exit codes, XML, runtime version, four Java-source hashes and the machine-readable result are retained under `../evidence/java-*`. Test duration in raw console/XML is an observation, not a framework benchmark.

## What loads and what is asserted

- `@SpringJUnitConfig(Config.class)` combines Spring's JUnit Jupiter extension with context configuration. JUnit creates the test instance; Spring TestContext supplies the `@Autowired ApplicationContext` field.
- `Config` declares a default-singleton `Repo` bean named `repo` and an `OrderService` bean named `service`. Spring supplies the repository to the factory method and service constructor.
- The test retrieves by **type**, using `ctx.getBean(OrderService.class)` and `ctx.getBean(Repo.class)`. A missing/ambiguous required result fails the test rather than silently returning null.
- `assertSame(repo, service.repository())` checks object identity, not value equality or merely the collaborator's type.
- `@DirtiesContext(AFTER_CLASS)` makes this self-contained demo explicitly release its framework-owned context afterward. The test does not manually close it. Ordinary non-mutating smoke tests can use Spring's context cache; this annotation is not a general requirement to reload every test.

`OrderService.repository()` is exposed solely to keep the small wiring assertion explicit. The collaborators have no order-processing or database implementation; a smoke-test pass must not be presented as proof that those behaviors work.

## Documentation and licensing

`fetch-docs.py` reproduces six official pages and eight exact claim excerpts. Sources include Spring6.2.11 `SpringJUnitConfig`, `SpringExtension`, `ContextConfiguration`, `DirtiesContext` and `BeanFactory`, plus JUnit5.12.2 `Assertions.assertSame`. Actual HTTP status, resolved URLs, hashes and text/HTML are retained in `java-doc-*` evidence.

JAR licenses/notices are extracted into `licenses/`, including the newly used Spring Test module; ECJ's EPL2.0 evidence is retained separately. Dependencies, hashes and download code preserve reproduction. Do not infer a Spring Boot integration or comprehensive application test from this selected-configuration example.
