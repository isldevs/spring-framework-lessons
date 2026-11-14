# Technical verification notes

Actual execution completed successfully with compiler and Java process exit codes **0**, empty compiler/runtime stderr, and dependency SHA-256 validation exit **0**. `../evidence/java-verification-result.json` stores the measured results, source hashes and exact stdout. Each phase's command, exit code, stdout and stderr are retained separately. Run `python source/java/verify.py` from the lesson directory to recreate them.

## What is actually demonstrated

1. The application supplies `Config.class` to an annotation configuration context via register/refresh.
2. `@ComponentScan("lesson.di")` finds the `@Repository Repo` and `@Service OrderService` candidates in that configured package and registers bean definitions. A metadata-only postprocessor observes both definitions before either application component's constructor event.
3. OrderService has one constructor requiring Repo. There is one Repo candidate. Spring uses that constructor and supplies the repository reference; the constructor does not call getBean or create its dependency.
4. Repo's construction is observed before the OrderService constructor receives it. Both events precede `context ready` and application use.
5. `service.repo() == context.getBean(Repo.class)` is true. `service.useRepository()` returns `ready` by calling its injected Repo. Repeated OrderService lookup returns the same default-singleton service and does not rebuild the graph.

Spring's internal infrastructure objects are not the subject of the construction trace; the ordering assertions concern the demonstrated Repo/OrderService graph. Scanning, bean definitions and runtime instances are different stages. A definition is metadata, not an already-constructed service. Do not show the application using the service before the reference has been injected.

No `@Bean` factory method is used in this lesson. This differs from the prior Java-configuration factory example: here, stereotype scanning plus constructor autowiring is the mechanism. No `@Autowired` annotation is required for the single-constructor case, but this is not a claim that every overloaded-constructor arrangement is resolved automatically.

## Official documentation actually consulted

- https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html — automatic detection and registration of stereotyped classes, and default candidate annotations including `@Repository` and `@Service`.
- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired.html — “If a class only declares a single constructor to begin with, it will always be used, even if not annotated.”
- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html — type-driven injection and optional semantic qualifiers.
- https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html — container-supplied dependencies when creating a bean.

All four fetched sources returned HTTP 200. HTML snapshots, extracted text and exact supporting quote contexts are retained under `../evidence/java-official-*`. The reference pages establish framework semantics; the pinned Spring 6.2.11 execution establishes that this actual example behaves as described.

## Production-safe claims

“Configured scanning finds annotated classes and registers definitions.”

“Spring resolves this constructor's Repo parameter by type.”

“Spring creates the repository and passes its reference to OrderService.”

“In this default-singleton run, the graph is wired before application use.”

“same Repo bean: true” and “application result: ready” are excerpts of the actual stdout, not fabricated terminal results.
