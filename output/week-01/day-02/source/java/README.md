# Spring constructor-injection example

This example runs actual Spring component scanning and single-constructor dependency injection. It has no Spring Boot or web-server dependency.

From the lesson directory:

```sh
bash source/java/run.sh
# Also regenerate separated compiler/runtime/command evidence:
python source/java/verify.py
```

The supplied runtime dependencies are SHA-256 pinned in `dependencies.sha256`. If any are missing, `run.sh` invokes `fetch-dependencies.py` to download the pinned Maven coordinates and validate their published SHA-1 checksums before creating a fresh SHA-256 manifest. With the retained libraries present and valid, `run.sh` and `verify.py` need no network.

Toolchain actually used: OpenJDK **21.0.13**, Eclipse ECJ **3.40.0**, Java 17 class-file target, Spring Framework **6.2.11**, Micrometer observation/commons **1.14.11**. ECJ is used because the environment has a Java runtime without javac. Dependency license and notice texts are retained in `licenses/`; the project example license is preserved from the existing example.

## Actual code and mechanism

- `src/lesson/di/Config.java`: `@Configuration` with `@ComponentScan("lesson.di")` configures the scan scope.
- `Repo.java`: `@Repository` marks the concrete dependency as a component candidate.
- `OrderService.java`: `@Service` marks the dependent service. Its **only** constructor requires a `Repo`; no `@Autowired` annotation is necessary for this single-constructor case.
- `DiDemo.java`: registers `Config.class`, installs a diagnostic observer, and refreshes the annotation context. This explicit registration/refresh sequence permits observing scanned definitions before singleton creation. It has the same configured startup role as the constructor convenience `new AnnotationConfigApplicationContext(Config.class)`.

The diagnostic BeanFactoryPostProcessor checks only metadata and records the two scanned definition names. It never requests a bean. Spring then resolves the unique Repo type, creates Repo, and passes that reference to the OrderService constructor before context startup returns. Only afterward does the application call getBean and use the injected repository.

Actual successful output:

```text
App starts Spring with Config.class
definitions registered: repo, orderService
Repo created
OrderService constructed with Repo
context ready
same Repo bean: true
application result: ready
scanned definitions: repo, orderService
```

The program asserts discovery before constructor events, Repo before OrderService, a wired service before context readiness, identity with the container's repository bean, stable default-singleton lookup, one unambiguous Repo candidate and successful repository use. A failing assertion makes the process fail; the output is not hard-coded success text.

This example uses non-lazy default singletons. Do not generalize its startup timing to prototype, lazy or other scoped beans. Type matching is unambiguous because exactly one Repo candidate exists; multiple candidates need the appropriate qualification or selection rules.

Actual evidence is in `../evidence/java-*`. Official documentation URLs and verbatim contexts are retained in `java-official-claims.json` and `java-official-documentation.json` there. See `technical-notes.md` for interpretation and production wording.
