# Actual Spring bean-naming example

This project uses real Spring Framework **6.2.11** to separate bean identity, type matching and injection qualifiers. `AlphaConfig` explicitly names the `Client` returned by its `client()` method **alpha**. Its Java method name is not an additional bean name. `BetaConfig` names its `backup()` result **beta**. Both names identify default singleton beans of the same concrete `Client` type.

The markers alpha/beta are ordinary local identifiers; no remote connection, benchmark or performance claim is involved.

## Reproduce

From the lesson directory:

```sh
bash source/java/run.sh
```

From this directory, `./run.sh` is equivalent. Requirements are Python3 and a Java17-or-newer runtime. The actual verification used OpenJDK21.0.13. Pinned Eclipse ECJ3.40.0 compiles Java17-target classes without installed javac or Maven. Spring Boot is not used.

`lib/` contains ten pinned compiler/runtime/test jars. Their coordinates, source URLs, hashes and third-party notices are retained in `dependency-sources.json`, `dependencies.sha256` and `licenses/`. The dependency manifest is actually checked before compilation. `fetch-dependencies.py` can recreate these fixed dependencies from Maven Central and checks its published checksums.

`verify.py` compiles main and test sources separately, executes JUnit and runs `NamingDemo`. Exact commands, exit codes, stdout/stderr, Java version, source hashes and JUnit XML are retained under `../evidence/java-*`.

## Four actual tests

1. A context containing only AlphaConfig verifies the explicit alpha definition and factory method metadata, absence of a client bean ID, and identity across getBean("alpha"), getBean("alpha", Client.class) and getBean(Client.class).
2. A fresh context containing AlphaConfig and BetaConfig verifies two distinct named Client instances, no primary flag on either definition and a NoUniqueBeanDefinitionException containing both names for getBean(Client.class).
3. Named lookup with a required type checks the selected bean. Requesting alpha as String throws BeanNotOfRequiredTypeException with the selected name and actual/required classes; alpha with Client succeeds.
4. A separate consumer receives beta through a constructor parameter annotated @Qualifier("beta"). The unqualified getBean(Client.class) call in that same context remains ambiguous. The injection metadata and the name-based lookup API perform distinct jobs.

Actual result: **4 tests found,4 started,4 successful,0 failed**. Main compilation, test compilation, JUnit and standalone execution all exited0, with empty stderr. Passing assertions, rather than invented console labels, establish these facts.

## Actual application output

```text
named alpha: alpha
typed name alpha: alpha
single type same: true
named beta: beta
type lookup: NoUniqueBeanDefinitionException
type candidates: 2
type message: No qualifying bean of type 'lesson.naming.Client' available: expected single matching bean but found 2: alpha,beta
```

The single-bean and two-bean cases use separate fresh contexts. The example does not refresh an already refreshed GenericApplicationContext or dynamically add BetaConfig to an existing refreshed example. The animation's sequence compares those configurations.

Names identify beans. Distinct names alone do not select between these two equally eligible Client beans for a type-only query. This is a scoped example without primary/priority preferences; it does not claim every multi-bean type lookup must fail. Qualifier matching belongs to type-driven injection selection and should not be described as the same API as getBean(String).

## Documentation and rights

Seven official Spring API6.2.11/reference6.2 pages were actually fetched with HTTP200. Their resolved URLs, response SHA-256, HTML/text and supported exact excerpts are retained under `../evidence/java-doc-*`. They cover explicit @Bean names, BeanFactory's three lookup forms, ambiguity, required type checks and qualifier injection semantics. The example source license and all dependency notices are retained.
