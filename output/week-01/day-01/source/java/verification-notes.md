# Actual Java/Spring verification

Executed successfully in the shared environment on 2026-11-13, for the requested production schedule date 2026-11-16. The schedule is not a claim about when tests ran.

OpenJDK 21.0.13 (Debian 21.0.13+9-1-deb13u2-Debian), ECJ 3.40.0, Java 17 target, Spring Framework 6.2.11. Dependency versions are fixed in `fetch-dependencies.py`. Run command: `./run.sh`. Exit status: 0. Compiler/runtime stderr: empty in the final successful run.

Actual program output:

```
manual wiring: true
spring wiring: true
same singleton: true
unmanaged same as bean: false
```

`source/evidence/java-program.stdout.txt` contains output from a separate successful direct Java execution; `java-run.stdout.txt` contains dependency validation plus output; `java-run.stderr.txt` is empty; `java-version.txt` records the runtime. Identity comparisons are backed by explicit throwing assertions.

Verified:
- Manually constructed Service receives the manually constructed Repo.
- Spring passes the registered Repo bean into the Service factory method; the returned Service contains that exact reference.
- Repeated lookup of this default singleton Service returns the same instance.
- A separate `new Repo()` is distinct from the managed bean.

Official sources consulted (downloaded HTML snapshots and extracted passages retained under `source/evidence/java-*`):
- https://docs.spring.io/spring-framework/reference/core/beans/introduction.html — DI is a specialized form of IoC; the container injects dependencies as it creates a bean; a bean is an object instantiated, assembled and managed by the container.
- https://docs.spring.io/spring-framework/reference/core/beans/java/bean-annotation.html — @Bean method parameters describe dependencies, resolved similarly to constructor injection.
- https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html — singleton is the default scope, per bean definition, per container.

The live reference pages can track newer releases. Runtime behavior here was tested against the explicitly pinned 6.2.11 jars. This does not claim every Java object is created by Spring or that every getBean invocation constructs a fresh instance. Factories explicitly call `new`; the container controls their invocation and resolves dependencies.
