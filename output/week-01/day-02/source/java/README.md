# Actual ApplicationContext example

This minimal project uses **Spring Framework 6.2.11** and the concrete `AnnotationConfigApplicationContext`. It is not a Spring Boot application. The public demo types are `Config`, `Repo`, `Service`, `DemoEvent` and `ContextDemo`, all in `lesson.context`.

The app explicitly creates a no-argument context, registers `Config.class`, calls `refresh()`, retrieves a `Service`, publishes a custom event and closes the context with try-with-resources. `Config` declares `@Bean Repo repo()` and `@Bean Service service(Repo repo)`. The context resolves the Repo argument and manages the resulting Service.

## Reproduce

From the lesson directory:

```sh
bash source/java/run.sh
```

From this Java source directory, `./run.sh` is equivalent. Requirements are Python3 and a Java runtime17 or newer. The verified runtime is OpenJDK21.0.13. Maven and javac are not installed and are not claimed as used. Pinned Eclipse ECJ3.40.0 compiles Java17-target classes. The included ten jars and `dependencies.sha256` allow this exact classpath to be checked and run offline; `fetch-dependencies.py` recreates the pinned jars from Maven Central and verifies published SHA-1 plus retained SHA-256 hashes.

`verify.py` checks dependencies, separately compiles production/test Java sources, runs the actual JUnit Platform Console and executes the standalone `ContextDemo`. Commands, stdout, stderr, exit codes, Java version, JUnit XML and source hashes are retained under `../evidence/java-*`.

Actual result: **2 JUnit tests found, 2 successful, 0 failed**. Both compilations, JUnit and the application exited0 with empty stderr. These results describe the included runner; no Maven invocation is claimed.

## What is genuinely verified

1. `definitionsPrecedeSingletonsAndContextProvidesLookupEventsAndCleanup` registers configuration while the context is inactive and observes no Repo/Service constructors yet. A programmatically registered `BeanFactoryPostProcessor` inspects the application BeanDefinitions after configuration processing during `refresh()`, when the Repo and Service singleton objects do not yet exist. After refresh, it checks one instance of each, dependency identity, constructor order, repeated lookup identity and the real business result. One explicit `DemoEvent` reaches the managed Service listener. Closing runs its `DisposableBean.destroy()` once, and repeated close does not repeat cleanup.
2. `lazyDefinitionDoesNotImplyAnInstanceExistsAfterRefresh` demonstrates the important exception: a separate `@Lazy` bean has a definition but no singleton instance after refresh. Its first lookup constructs it once, and repeated lookup returns that same instance. This guards against generalizing the main eager-singleton illustration to all definitions.

Actual concise proof lines:

```text
same service: true
events handled: 1
cleanup called: true
```

The actual standalone app additionally prints:

```text
context created
configuration registered
bean definitions: repo, service
instances at definition stage: 0
repo created
service created with repo
context refreshed
same service: true
service result: hello from repo
events handled: 1
service cleanup
cleanup called: true
```

These lines are actual captured output, backed by meaningful assertions in the tests. The small global Trace counters are single-threaded demonstration instrumentation, not production concurrency code or benchmark measurements.

## Important boundaries

- `register(Config.class)` initially registers configuration metadata. The two `@Bean` definitions are discovered during configuration processing inside `refresh()`. Do not claim both application definitions existed immediately at `register` time.
- BeanDefinitions are metadata describing bean construction and properties, not the instantiated objects. ApplicationContext delegates bean-definition and singleton management to its BeanFactory. The visual context boundary contains that machinery, not a claim that definitions and objects are one map or public fields.
- Spring creates the main example's default non-lazy singleton Repo and Service during refresh. It does not follow that every definition always creates an object at refresh, nor that every Java object is a managed bean.
- `getBean(Service.class)` is a lookup here, after initialization. It returns the same managed Service rather than rebuilding it on each call. The Repo reference was already supplied during service creation.
- Service implements `ApplicationListener<DemoEvent>` so the single event count excludes Spring's own context events. The example's default event multicaster delivers synchronously. The event-publisher API does not promise synchronous/immediate delivery for every custom multicaster or asynchronous listener arrangement.
- Service implements `DisposableBean`; cleanup on close is verified for this managed singleton. Prototype destruction is not automatically managed in the same way. Do not claim the JVM object or every object is deleted by `close()`.

## Documentation and rights

Actual official Spring6.2 reference and exact6.2.11 API pages were retrieved with HTTP200 and retained under `../evidence/java-doc-*`, including HTML/text, URL/hash records and direct claim excerpts. See `java-doc-notes.md` for supported qualifications. Source/dependency hashes and Maven Central coordinates are retained here; jar notices and ECJ's EPL-2.0 evidence are under `licenses/`. Spring and Micrometer components are Apache-2.0; ECJ and JUnit/bundled library notices are retained separately.
