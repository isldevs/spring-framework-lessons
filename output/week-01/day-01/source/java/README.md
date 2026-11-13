# Spring IoC: manual construction vs managed beans

Run `./run.sh`. Requires Python 3, a Java 17+ runtime and outbound HTTPS to Maven Central on the first run. The script downloads pinned jars, verifies Maven Central's published SHA-1, compiles the Java source with open-source Eclipse ECJ, and executes with Java. `dependencies.sha256` additionally records SHA-256 for downloaded files. Dependencies and generated `.class` files are retained so the verified example is also runnable offline with `java -cp 'build:lib/*' IoCDemo` from this directory.

The machine provides OpenJDK 21.0.13, without javac; ECJ 3.40.0 compiles to Java 17 class format. Spring Framework is 6.2.11. Micrometer observation/commons are 1.14.11. No Spring Boot or web server is needed.

`@Configuration` registers two `@Bean` factory methods. Spring resolves the `Repo` parameter when it invokes `service(Repo repo)`, then that factory method constructs `Service` with the dependency. `getBean(Service.class)` returns the default singleton already created during context refresh. The example deliberately retains `new` inside the factory methods: IoC does not mean all Java `new` expressions vanish.

The unregistered `new Repo()` in `main` remains an ordinary independently created Java object. Spring manages objects registered with its container; this does not mean Spring creates every Java object.

Identity assertions fail with a nonzero exit if manual wiring, Spring wiring, default singleton reuse, or independent object identity is incorrect. This is a focused runnable demonstration. `getBean` is shown at the application boundary; services usually receive dependencies through injection rather than looking them up themselves.

## Licensing

Original example and build script: MIT (see LICENSE). Spring Framework and Micrometer: Apache License 2.0. Eclipse JDT ECJ: Eclipse Public License 2.0, as listed in its published POM; ECJ is a build-time tool. All permit commercial use. Dependency notices, license text, and ECJ's published POM are retained in `licenses/`; jars retain their upstream metadata. OpenJDK runtime is system provided under GPLv2 with the Classpath Exception. This example adds no third-party visual/audio asset to the video.
