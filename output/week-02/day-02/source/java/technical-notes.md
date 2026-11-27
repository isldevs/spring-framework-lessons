# Technical scope and verification

The required dependency is `PaymentGateway`, taken from the managed service's single constructor. Registration is explicit through a configuration class plus `@Import`; component scanning is not claimed.

In this controlled Spring6.2.11 example, the parameter name is `gateway`, and the same-named bean is an incompatible `AuditLogger`. The implementation's name shortcut requires a type match, so it does not resolve that bean. The observed factory then enumerates two compatible names and excludes `backupGateway` because its definition has `autowireCandidate=false`. Exactly one eligible gateway remains and is injected. An `assertSame` proves the stored dependency is that same managed instance.

Compatible type names and eligible autowire candidates are different sets. Disabling autowiring does not erase a definition or prevent explicit retrieval. The extra negative test leaves only that disabled matching definition and verifies that startup still fails for a required constructor dependency.

The two negative refresh attempts are expected to log warning messages. Each actual exception is asserted as `UnsatisfiedDependencyException` with deepest `NoSuchBeanDefinitionException` cause and an inactive context after cancellation. This is verification of the example, not a statement that every missing dependency fails immediately at startup; lazy/optional injection and other mechanisms differ.

The observer records actual delegated method results. Its preliminary `getBeanNamesForType` observation is a compatible-name measurement, not a claim that this is the framework's exact internal candidate-enumeration API or the entire resolution algorithm. The inspected implementation uses `BeanFactoryUtils.beanNamesForTypeIncludingAncestors`; this example has no parent factory and no `FactoryBean`.

Qualifiers, primary/fallback status, names, collections, generics, lazy providers, self references and parent factories can affect other resolution paths. Official reference pages document some of these options, and the version-matched implementation notes capture shortcut and full-search branches. The narration should say "in this example" when presenting the measured two-to-one candidate result and must not say "Spring always injects by name" or "Spring only checks type".

This JUnit project uses real `AnnotationConfigApplicationContext` registration/refresh/close calls. It does not claim `@SpringJUnitConfig`, Spring Boot startup, scanning, a main application run, a network call, a real payment or a performance measurement.
