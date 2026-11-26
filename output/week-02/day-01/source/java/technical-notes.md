# Technical scope — Constructor injection

Approved curriculum: Constructor injection, publication2026-11-23, proposed19:00Asia/Phnom_Penh. Internal schedule identifiers are not on-screen numbering.

The real verification is JUnit/Spring TestContext execution, not a separate application main. `Config` explicitly imports `OrderService` and `DemoPaymentGateway`. Those regular component classes become registered bean definitions; the default singleton instances are created through Spring. The service's single constructor requires `PaymentGateway`, and the only matching registered implementation is selected. Spring supplies that exact object to the constructor. No `@Autowired` annotation is present on the service constructor.

The fixture itself is made by JUnit; Spring TestContext injects its `ApplicationContext` field. Do not confuse that fixture annotation with the absence of an annotation on `OrderService(PaymentGateway gateway)`. The test does not assert the concrete ApplicationContext implementation type. It retrieves by type, not by an assumed `orderService` or gateway bean name.

Two actual JUnit tests passed. The managed test asserts Spring version, exactly one service constructor, no constructor `@Autowired`, the declared parameter type, exactly one gateway candidate, reference identity and service execution returning `demo-paid:2500`. The manual control constructs its own gateway and service, proving those instances remain distinct from the Spring-managed singletons. Raw JUnit proof lines are emitted only after their assertions pass; exact output and five tested-source hashes are retained.

Default singleton scope is part of this example's identity expectation. `DemoPaymentGateway` does not contact a payment provider or move money. Its output is a deterministic demonstration string; the test only proves that this service delegates to that actual injected collaborator for the asserted input. It is not evidence of real transaction processing or whole-application correctness.

The supported no-annotation inference is scoped to Spring-managed classes with one constructor in the verified modern Spring version. The official Spring6.2 reference records introduction in4.3. This lesson makes no general claim that arbitrary objects created with `new` are injected, nor that all multiple-constructor or multi-candidate cases resolve identically.

The context lifecycle remains framework-owned, with AFTER_CLASS DirtiesContext for explicit demo cleanup. Context caching and production component scanning are separate concerns; this project imports the two classes explicitly. Video animation times illustrate causality and never represent measured framework execution performance.
