# Actual Spring Boot constructor-injection example

This example starts a real **Spring Boot 3.5.6** application, rather than a bare Spring context labelled as Boot. `CheckoutApplication` has `@SpringBootApplication` and starts a non-web `SpringApplication`. Its application package `lesson.orders` is scanned, finding `@Component DemoGateway` and `@Service OrderService`.

`OrderService` declares a `private final PaymentGateway gateway` and one constructor receiving that interface. Spring can use the sole constructor without an `@Autowired` annotation. The current application has one matching implementation, so the dependency is unambiguous. A `final` field prevents reassignment of this reference; it does not make the gateway's internal state immutable.

`placeOrder(orderId, amountCents)` validates the arguments and delegates to the supplied gateway. `DemoGateway` only formats an in-memory simulated approval and counts calls. **No payment processor is contacted and no money moves.**

## Reproduce

Requirements: Python 3 and a Java runtime 17 or newer. The verified environment is OpenJDK 21.0.13. Maven and javac are not required by this runner: Eclipse ECJ 3.40.0 compiles Java17-target classes.

```sh
bash source/java/run.sh
```

From this source directory, `./run.sh` is equivalent. `fetch-dependencies.py` downloads fixed Maven Central coordinates, verifies published SHA-1 checksums, records SHA-256 hashes and retains jar license/notice evidence. `verify.py` then checks that manifest, compiles main and test sources separately, executes JUnit and runs the standalone Boot application. All actual commands/stdout/stderr/exit codes are retained in `../evidence/java-*`.

The pinned versions are coherent with the retained Spring Boot 3.5.6 BOM: Spring Framework 6.2.11, Micrometer 1.15.4, SnakeYAML 2.4, JUnit Jupiter 5.12.2 (console standalone/platform 1.12.2). `lib/` includes the compiler and fixed runtime/test jars so the exact verified run can be repeated offline after download.

## Two actual tests

1. `bootInjectsTheManagedGatewayBeforeOrderUse` starts Boot, verifies its actual runtime version, checks one gateway candidate and identity of the injected/managed reference, and verifies gateway construction and service constructor invocation precede context readiness. It then places a simulated order, verifies the exact receipt, verifies one gateway call and reuses the default singleton service.
2. `aRecordingFakeTestsOrderForwardingWithoutSpring` manually supplies a recording fake to the same OrderService constructor. It verifies the order ID, amount in cents, call count and returned fake approval. This is a separate pure Java service test, not another Spring-managed gateway bean.

Actual JUnit result: **2 tests found, 2 started, 2 successful, 0 failed**. Compile/test/standalone application all returned exit0 with empty stderr. JUnit XML reports are retained both in build/test-results and as evidence.

Actual proof lines:

```text
same gateway bean: true
receipt: APPROVED order-1042 USD 19.99
Spring Boot integration test: passed
fake gateway test: passed
```

The receipt describes the local demo outcome only. The simulated gateway constructor runs before the service constructor, which stores its supplied reference before any order is placed. This default non-lazy singleton example does not claim every scope/lazy arrangement initializes before lookup.

## Documentation and rights

Versioned official Spring Boot 3.5 dependency-injection and SpringApplication documentation, plus Spring Framework single-constructor guidance, are saved in `../evidence/java-doc-*`. Their source URLs, HTTP statuses, SHA-256s and small verbatim claim excerpts are retained. Dependency source URLs and SHA-256s are in `dependency-sources.json` and `dependencies.sha256`; third-party licenses/notices are in `licenses/`.
