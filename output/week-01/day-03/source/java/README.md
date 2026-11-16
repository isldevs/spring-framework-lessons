# Actual Spring bean-registration example

This minimal project demonstrates two valid registration paths with **Spring Framework 6.2.11**. It does not use Spring Boot. `Client` is an ordinary unannotated Java class. A refreshed context with no application configuration cannot retrieve it. Registering `FactoryConfig` supplies its `@Bean Client client()` method; Spring records factory-method metadata and later calls that method to obtain the managed Client.

The second context registers `ScanConfig`, whose `@ComponentScan("lesson.scan")` discovers `@Component Worker` in that package. `@Component Outside` is on the same Java classpath in `lesson.outside`, but lies outside this configured scan and is not registered through another route. It therefore remains unavailable in this example. The annotation makes a class a scanning candidate; it does not make every context discover every annotated class.

These are two demonstrated registration paths, not an exhaustive list. Explicit programmatic registration, imports and other supported configuration mechanisms are outside this short lesson. Client and Worker are different demo bean types in separate contexts, not two instances of one bean or two competing registrations.

## Reproduce

Requirements: Python 3 and a Java runtime 17 or newer. The verified environment is OpenJDK 21.0.13. Eclipse ECJ 3.40.0 compiles Java17-target classes, so the provided runner does not require installed Maven or javac.

From the lesson directory:

```sh
bash source/java/run.sh
```

From this Java directory, `./run.sh` is equivalent. `verify.py` checks `dependencies.sha256`, compiles main and test sources separately, runs JUnit and executes the standalone `lesson.registration.RegistrationDemo`. All actual commands, stdout, stderr and exit codes remain in `../evidence/java-*`.

Ten fixed jars are included under `lib/`: Spring Framework 6.2.11 modules, Micrometer 1.15.4, ECJ 3.40.0 and JUnit Platform Console Standalone 1.12.2 (Jupiter 5.12.2). `fetch-dependencies.py` can download them again from Maven Central, checks published SHA-1 checksums, records SHA-256, and extracts their license/notice files. The current ten jars were checked against published checksums during this production, not merely copied without verification. `dependency-sources.json` records coordinates and provenance.

## Three actual tests

1. `aPlainClasspathClassHasNoDefinitionOrManagedInstance` refreshes an AnnotationConfigApplicationContext without application configuration. It checks the actual Spring version, no Client definition or singleton, an expected `NoSuchBeanDefinitionException` from Client lookup, and zero Client constructor calls. The negative case is an expected assertion, not an uncaught failure.
2. `registeredConfigurationAddsAFactoryDefinitionAndRetrievableSingleton` registers FactoryConfig, then observes the `client` definition inside refresh before Client construction. Its metadata points to factory bean `factoryConfig` and factory method `client`. After refresh, lookup by type/name returns the same Client, its method returns `explicit`, and the constructor/factory each ran once.
3. `configuredScanRegistersItsComponentAndExcludesAnAnnotatedOutsideClass` registers ScanConfig and observes Worker metadata before construction. After refresh, Worker is retrievable by type/name and is the same singleton; its method returns `scanned`. Outside is demonstrably annotated but has no definition and produces the expected missing-bean exception because its package was not scanned. Its constructor never runs.

Actual JUnit result: **3 tests found, 3 started, 3 successful, 0 failed**. Main compilation, test compilation, JUnit and standalone execution all exited **0**, with empty stderr. JUnit XML reports and actual source hashes are retained alongside command evidence.

Actual captured proof lines include:

```text
plain class missing: true
@Bean definition before instance: true
@Bean retrieved: true
scan definition before instance: true
scan retrieved: true
outside scan missing: true
```

The standalone application also captures `@Bean definition: client`, `@Bean factory called`, `Client created`, `scan definition: worker` and `Worker created` in that order within their respective contexts. `java-verification-result.json` records the actual full output and test summary.

## Registration, construction and scope

`ctx.register(FactoryConfig.class)` adds configuration metadata to a new unrefreshed context. During `refresh()`, configuration processing discovers the @Bean method and creates its bean definition. A BeanFactoryPostProcessor observes this metadata without calling getBean or otherwise triggering Client construction. Spring then invokes the factory to create this example's default non-lazy singleton. Scanning likewise registers Worker metadata before its constructor runs.

The context already contains infrastructure definitions; diagrams focus on these demo application beans. The tests do not claim every bean is eagerly constructed, that all Java classes become beans, that scanning covers packages outside its configured boundary, or that only these two registration mechanisms exist. Default singleton identity and creation timing here do not describe every scope or lazy arrangement.

## Documentation and rights

Eight official Spring pages were actually retrieved with HTTP200. Versioned 6.2.11 API pages and Spring 6.2 reference pages, hashes, HTML/text and relevant claim excerpts are retained under `../evidence/java-doc-*`. Recommended publishing references verified during this production:

- https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/6.2/core/beans/classpath-scanning.html

Project code is under the retained MIT license. Third-party compiler/runtime/test notices are under `licenses/`. No external service, paid tool or fabricated result is involved in executing this example.
