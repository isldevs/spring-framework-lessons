# Technical verification notes

The verified startup uses `new SpringApplication(CheckoutApplication.class)` and `run(...)` with `WebApplicationType.NONE`. `@SpringBootApplication(proxyBeanMethods = false)` remains the actual Boot entry annotation; disabling proxying does not remove scanning or auto-configuration. No HTTP server is started.

The code uses constructor injection into a final field, through the PaymentGateway interface. DemoGateway is a single scanned component implementing that interface. OrderService has a sole constructor and no field/setter injection or @Autowired annotation. Spring supplies an existing managed candidate reference as a constructor argument. With multiple candidates, disambiguation would be necessary; this example intentionally has one.

The integration test calls actual SpringApplication startup, verifies `SpringBootVersion.getVersion()` equals3.5.6, obtains the context-managed service and interface bean and checks their identity. Trace ordering asserts DemoGateway creation precedes service construction and both precede context-ready. The gateway call count is zero until the first order, then one. The second lookup returns the same service singleton. Thus dependency injection is verified before business use, not inferred from annotation presence.

The separate fake test invokes the public constructor directly and verifies externally observable delegation: order ID, cents, exactly one call and returned fake response. The fake is not annotated and is not a component-scan candidate. No mocking library is required.

The actual receipt is `APPROVED order-1042 USD 19.99`. It is generated in memory using Locale.ROOT and integer cents. This is a pedagogical payment port/adapter scenario, with no credential, payment network or real financial action.

The runner uses ECJ because javac and Maven are absent in this environment. It compiles against pinned real Boot/Framework jars and executes JUnit ConsoleLauncher. JUnit XML and raw output are evidence; results are not fabricated. Logging/banner suppression only removes unrelated startup noise. All actual main/test compilation and test/application processes exited0 with empty stderr.

Consult `../evidence/java-verification-result.json` for actual values and source hashes. Official docs explicitly recommend constructor injection, state a single constructor works without @Autowired, and support non-web SpringApplication startup for a JUnit test. A final dependency reference cannot be reassigned, but the supplied object may be mutable.
