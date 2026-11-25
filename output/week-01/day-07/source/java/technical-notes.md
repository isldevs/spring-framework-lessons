# Technical scope and evidence

Approved topic: **Context smoke test**. Approved publication date **2026-11-22**, proposed19:00Asia/Phnom_Penh. These internal schedule fields are not on-screen numbering.

## Runtime mechanism

JUnit Jupiter discovers `ContextSmokeTest.contextLoadsAndWires()`. The class-level `@SpringJUnitConfig(Config.class)` provides `SpringExtension` and configuration metadata. Spring TestContext obtains a context for that configuration and injects its reference into the test's `@Autowired ctx` field. Its context-loading/caching machinery owns the context; this example does not assert a concrete `AnnotationConfigApplicationContext` implementation and does not claim a fresh context is created before every test method.

The selected default non-lazy singleton configuration creates `Repo`, then calls the service factory with that managed dependency, which is supplied through the `OrderService` constructor. The test's required typed lookups select the configured beans. Both returned references are non-null, and identity comparison verifies that the service's collaborator is the repository from this context. Exact bean names follow factory methods: `repo` and `service`; a name-based `getBean("orderService")` is not part of this example.

The `@DirtiesContext(AFTER_CLASS)` declaration performs explicit demo cleanup through the framework. The official documentation normally recommends dirtying contexts when tests modify their state. This unmodified example could instead retain Spring's cache in a larger suite; cleanup is not advertised as a universal smoke-test requirement.

## What was actually executed

- Eleven pinned JARs were obtained/revalidated against published SHA-1 and a local SHA-256 manifest.
- ECJ actually compiled three main Java files and one test class, targeting Java17 on the captured JDK.
- One JUnit test was discovered, started and succeeded. JUnit XML reports zero skipped, failed or error cases.
- Raw proof is `bean found: true` and `wiring same: true`, printed only after assertions pass. No standalone application execution or application stdout is fabricated.
- Source hashes in `java-verification-result.json` identify the exact tested Java files.
- Six official documentation pages were fetched with HTTP200, with HTML/text hashes and eight exact claim excerpts retained.

## Limits

The pass is evidence for **this loaded configuration, selected beans and stated wiring assertions**. It does not prove the entire production application is configured, lazy beans not requested by the test can work, business rules are correct, or a database/API call succeeds. The demo has no such implementation or assertions. The video's run/lookup/assert animations are explanatory edit timing, not measurements of Spring startup or test performance.
