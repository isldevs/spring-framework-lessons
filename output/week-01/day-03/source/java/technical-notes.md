# Bean-registration technical notes

Verified runtime: Spring Framework 6.2.11, Micrometer 1.15.4, OpenJDK 21.0.13. ECJ 3.40.0 compiled Java17-target classes. JUnit Jupiter 5.12.2 executes through console/platform 1.12.2. Ten pinned jars and their hashes/notices are retained. Maven, javac and Spring Boot were not used.

## Actual causal observations

- The negative lookup occurs only after refresh, so the expected error is `NoSuchBeanDefinitionException`, not a context-not-active error. Client is present on the Java classpath but has neither a definition nor a managed instance in that context.
- FactoryConfig is explicitly registered. Before refresh, its own definition exists but the method-derived `client` definition has not yet been processed. A non-instantiating BeanFactoryPostProcessor inside refresh observes `client` factory-method metadata while Client/factory counters remain zero. The factory and constructor then run once, and getBean returns that default singleton.
- ScanConfig explicitly scans `lesson.scan`. Worker has class-based definition metadata and no factory method; its definition exists before its constructor runs. The annotated Outside class is in `lesson.outside` and remains absent without another registration mechanism. The two positive paths use separate contexts and different bean types.

These assertions establish registration-before-construction for the illustrated ordinary application beans. Infrastructure processing is intentionally not illustrated as an empty global registry. Default eager-singleton timing is qualified; the example is not a statement about every lazy/scope/custom-processor setup.

## Actual result and reproduction scope

Three JUnit tests passed; none failed. Main/test compile, JUnit and standalone application exit codes are all0 with empty stderr. The raw output, expected-exception assertions, XML, actual command arrays and source SHA-256s support each reported proof line. The diagrams' speech/edit times are production timing, not Java performance measurements.

The @Bean snippet can omit Trace instrumentation on screen while preserving the real factory operation: `@Bean public Client client() { return new Client(); }`. The scan snippet must preserve the actual package `lesson.scan` and actual Worker/Outside boundaries. A generic plain-class example does not imply unannotated classes can never be beans: the Client factory path demonstrates that they can.

The official evidence includes eight HTTP200 documents and nine matched claim excerpts. Both publishing URLs are real retrieved pages. These two registration paths are valid examples, not the only Spring registration APIs.
