# Verified Spring dependency resolution

This minimal Java project demonstrates how a managed `OrderService(PaymentGateway gateway)` receives one eligible `PaymentGateway`. Three actual JUnit tests cover successful resolution, absence of a matching type, and exclusion of a matching but disabled autowire candidate.

## Reproduce

From this directory, with Java17 or newer and Python3 installed:

```sh
./run.sh
```

`fetch-dependencies.py` retrieves the pinned dependencies if missing and verifies Maven Central's published SHA-1 before recording local SHA-256. `verify.py` verifies all local JAR hashes, clears compilation/test-report directories, compiles the main and test Java sources, runs JUnit and derives machine-readable evidence from the actual output and XML reports. No Maven installation, network request at runtime, payment service or external application is required.

The verified environment used OpenJDK21.0.13, Eclipse ECJ3.40.0 targeting Java17 with `-parameters`, Spring Framework/Spring Test6.2.11, JUnit Jupiter5.12.2 via Platform1.12.2 standalone console and Micrometer1.15.4. `dependency-sources.json` and `dependencies.sha256` pin all11 JARs.

## The controlled example

`SuccessConfig` imports `OrderService` and registers these definitions:

| Name | Declared type | Autowire eligible |
| --- | --- | --- |
| `eligibleGateway` | `PaymentGateway` | yes |
| `backupGateway` | `PaymentGateway` | no: `@Bean(autowireCandidate=false)` |
| `gateway` | `AuditLogger` | unrelated type |

The last bean intentionally shares the constructor parameter's name. It cannot satisfy the required `PaymentGateway` type. The backup remains a registered bean and can be retrieved explicitly by name; exclusion from autowiring does not remove it from the factory. The successful test asserts reference identity between the injected field and the explicitly retrieved `eligibleGateway`.

`TracingBeanFactory` delegates every resolution decision to Spring. Its observer overrides record actual compatible names, actual `isAutowireCandidate` returns and the resulting eligible map. The animation may simplify these observed steps, but must not present this path as every possible Spring resolution order. Spring6.2 also has name-based shortcuts that preserve type/eligibility constraints, and qualifiers or primary candidates can affect other examples.

`MissingConfig` has no compatible type. `OnlyDisabledConfig` has a compatible definition excluded from autowiring. Both actual refresh attempts throw `UnsatisfiedDependencyException` whose deepest cause is `NoSuchBeanDefinitionException`; both are asserted negative cases. Spring prints two expected refresh-cancellation warnings to captured JUnit stderr. Those warnings are retained rather than represented as empty stderr.

## Evidence

Evidence lives in `../evidence/java-*`: actual compile/JUnit commands and exit codes, stdout/stderr, JUnit XML, Java runtime version, source hashes, actual delegated runtime trace and `java-verification-result.json`. `fetch-docs.py` retrieves and hashes official API/reference evidence; `framework/fetch-implementation.py` retrieves the matching Spring source JAR and produces source inspection evidence. See `technical-notes.md` and `implementation-notes.md` for the technical limits.

No standalone application or real payment was executed. The tests demonstrate context wiring rather than production payment behavior, performance, all ambiguity rules or every Spring dependency type.

## Rights

Spring and Micrometer: Apache2.0. JUnit: EPL2.0; standalone-console bundled notices are retained. ECJ: EPL2.0. The actual license/notice files extracted from distributed JARs and Eclipse's official EPL text are in `licenses/`. The checked Spring implementation source retains its Apache2.0 headers and distributed Spring license/notice. The lesson Java/tests and observer code are original iSLDevs educational source.
