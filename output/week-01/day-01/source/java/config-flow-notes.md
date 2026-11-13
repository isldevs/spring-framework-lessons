# Config-to-bean execution trace

`ConfigFlowDemo.java` is an additional minimal example for the closing explanation. It leaves the original `IoCDemo.java`, `run.sh`, and pinned runtime jars unchanged.

Run from this directory:

```sh
./run-config-flow.sh
```

The script first verifies `dependencies.sha256`, uses the retained ECJ 3.40.0 compiler with a Java 17 target, then executes with the installed OpenJDK 21.0.13 and Spring 6.2.11 jars. It uses a temporary compilation directory, cleans that directory afterward, and requires no network access. Actual compiler/runtime stdout, stderr and exit codes are retained under `../evidence/config-java-*`.

## Actual successful output

```text
App starts Spring with Config.class
Spring instantiates Config
Spring calls Config.repo(): create Repo
Spring calls Config.service(repo): wire Repo into Service
Spring context is ready
App calls getBean(Service.class)
same Repo bean: true
App calls getBean(Service.class) again
same Service bean: true
factory calls after lookups: 2 (unchanged)
```

Both compilation and execution exited **0**, with empty stderr.

The application supplies `Config.class` to `new AnnotationConfigApplicationContext(Config.class)`. The configuration class declares the two `@Bean` factory methods. The trace records the Config constructor and the actual factory method invocations. The `Repo` factory runs before the `Service` factory; Spring supplies that repository as the `service(Repo repo)` parameter, and the factory passes it into the Service constructor. Both factories run before the context constructor returns and before the application asks for Service.

Assertions verify this order, the service's exact repository identity, the repeated service lookup identity, and an unchanged factory invocation count after both lookups. The application does not call either factory method directly.

This example uses non-lazy **default singleton** beans. Its startup sequence must not be generalized to every scope or lazy bean. `getBean` here retrieves the ready instance rather than creating a new object on each call. The trace instruments the user configuration constructor/methods and application boundaries, not every Spring internal annotation-parsing operation. Spring manages these registered beans, not every Java object.

Official context for the API and configuration semantics is already retained with the lesson's documentation evidence:

- https://docs.spring.io/spring-framework/reference/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/core/beans/introduction.html
