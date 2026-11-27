# Dependency resolution: implementation scope

Inspected Spring Framework **6.2.11**, pinned to the matching `spring-beans` source artifact. This record describes source inspection. Actual compiled test output and runtime tracing are separate evidence files.

The lesson demonstrates a required, singular `PaymentGateway` constructor parameter on a Spring-managed `OrderService`. The simplified visual flow is: required dependency → compatible registered types → eligible candidates → supplied constructor argument. This is an accurate explanation of the example's full-search path, not a complete universal ordering of every Spring lookup.

## What the pinned implementation does

- `AutowiredAnnotationBeanPostProcessor.determineCandidateConstructors` accepts a class's only constructor when it has parameters, without requiring `@Autowired` (`framework/AutowiredAnnotationBeanPostProcessor.java`, lines 450–452). This applies while Spring creates a managed bean; constructing an arbitrary object with Java `new` does not trigger this process.
- `DefaultListableBeanFactory.resolveDependency` handles optional/provider/lazy cases before delegating ordinary resolution (lines 1622–1644).
- `doResolveDependency` first considers a pre-resolved shortcut and suggested value, then a dependency-name or qualifier-suggested-name shortcut (lines 1648–1707). The name shortcut also requires type compatibility, autowire eligibility, and other checks. **Do not say Spring always searches by type first, or resolves solely by name.**
- If those shortcuts do not resolve the request, ordinary candidate search calls `findAutowireCandidates` (line 1714). That method discovers bean names for the required type, including ancestors when applicable (lines 1956–1960), and applies self-reference and autowire-candidate checks (lines 1973–1977). Fallback passes exist after an empty result (lines 1978–2002).
- Eligibility is delegated to a candidate resolver (lines 956–968). The base check reads the bean definition's `isAutowireCandidate` flag (`AutowireCandidateResolver.java`, lines 44–46). Annotation-aware resolution retains that check and can also apply generic-type and qualifier constraints (`GenericTypeAwareAutowireCandidateResolver.java`, lines 64–70; `QualifierAnnotationAutowireCandidateResolver.java`, lines 156–170).
- If exactly one match remains, `doResolveDependency` uses that candidate and resolves/validates the instance (lines 1748–1762). A required request with no candidate raises a missing-bean error (lines 1714–1726). Multiple candidates may require further selection or produce a non-unique error (lines 1731–1737).
- When multiple eligible candidates need selection, `determineAutowireCandidate` considers primary status, dependency/suggested names, priority, a unique default candidate, and directly registered resolvable dependencies (lines 2035–2080). Qualifier filtering is part of eligibility; qualifiers are not merely bean-name aliases. This lesson does not claim to enumerate or animate every supported resolution route.

## Why the example's names matter

The intended constructor parameter is named `gateway`. An unrelated `AuditLogger` bean is also named `gateway`, while the compatible beans are named `eligibleGateway` and `backupGateway`. The wrong-type `gateway` cannot pass `isTypeMatch` in the name shortcut (line 1691). The full-search path can therefore distinguish type discovery from eligibility: both payment gateway types can be registered while the backup's `autowireCandidate=false` excludes it from constructor autowiring. This flag does not mean the backup bean is unregistered or cannot be retrieved explicitly.

The final runtime trace and assertions must establish that the actual example takes this path; inspecting source alone does not establish its execution. A missing compatible bean and a registered but disabled compatible bean are different configurations that can both leave a required dependency unresolved.

## Reproduction and provenance

Run `python framework/fetch-implementation.py` from this directory (Python standard library and network access required). It downloads the official Maven Central source JAR, checks its published SHA-1 and the pinned SHA-256, extracts the retained sources, and writes verbatim line-numbered excerpts and machine-readable inspection evidence. The matching official binary JAR supplies the full license and notice because the source JAR contains only per-file license headers.

- Source artifact: <https://repo.maven.apache.org/maven2/org/springframework/spring-beans/6.2.11/spring-beans-6.2.11-sources.jar>
- Source SHA-256: `f5fcf8046c9f5e0ef7cd183d2ac6b0e5d23cd7f27c174234243c71a5e6399c75`
- Source files retain their original Apache-2.0 headers. Full terms and notice are in `framework/LICENSE.txt` and `framework/NOTICE.txt`.
- Artifact HTTP statuses, hashes, member names, and license provenance are recorded in `../evidence/java-implementation-sources.json` and `framework/license-provenance.json`.
- Exact excerpts and inspected source hashes are in `../evidence/java-implementation-inspection.json` and `../evidence/java-implementation-excerpts.md`.

No tests, service output, or runtime trace are fabricated by the source-fetching script.
