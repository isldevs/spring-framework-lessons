# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Dependency resolution
- Publish date: 2026-11-24 (Tuesday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared files only. No upload, scheduling or publication has been performed. Manual approval is required.

## Title

How Spring Finds Your Dependencies

## Description and hashtags

How does Spring know what to inject into a constructor?

This Spring-managed OrderService requests PaymentGateway. In our example, the bean factory discovers two compatible beans, filters out a backup marked autowireCandidate=false, and supplies the remaining eligible gateway. The backup is still a registered bean; it is simply excluded from autowiring. An unrelated logger named gateway does not match the required type.

Three real JUnit tests verify the exact injected reference, a missing-type startup failure, and a startup failure when the only matching bean is ineligible. The failures produce UnsatisfiedDependencyException with NoSuchBeanDefinitionException as the root cause.

This is a simplified, verified resolution path. Qualifiers, primary settings, injection-point names and other rules can also affect selection. Spring does not always resolve dependencies solely by name or solely by type.

Verified with Spring Framework 6.2.11 and JUnit 5.12.2. No real payment is processed.

Narration is AI-generated.

Official Spring references:
https://docs.spring.io/spring-framework/reference/6.2/core/beans/dependencies/factory-collaborators.html
https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired-qualifiers.html
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/support/DefaultListableBeanFactory.html

#DependencyInjection #SpringFramework #SpringBeans #Java #ConstructorInjection #Shorts #iSLDevs

## Tags (comma-separated)

dependency resolution, Spring Framework, dependency injection, Spring beans, constructor injection, PaymentGateway, OrderService, autowire candidate, bean factory, DefaultListableBeanFactory, NoSuchBeanDefinitionException, UnsatisfiedDependencyException, Java, JUnit 5, iSLDevs

## Pinned comment

Registered does not always mean eligible for autowiring.

Our backup PaymentGateway is registered, but autowireCandidate=false excludes it from this constructor dependency. The unrelated bean named gateway is not a PaymentGateway at all.

The verified outcome: two compatible types, one eligible candidate, and the same gateway reference injected into OrderService. Qualifiers, primary settings and other resolution rules still matter in other configurations.

## Manual thumbnail selection

Where the YouTube app's Shorts upload/edit flow offers thumbnail editing, open its thumbnail/frame selector and choose the recognizable opening composition from the first second. Confirm that “How Spring”, “Finds Your” and the blue “Dependencies” highlight remain readable in the displayed crop. Use cover.png only if that upload flow supports selecting a separate image. Controls differ by app/version; neither automatic selection nor availability is guaranteed.

## Manual upload confirmation

Confirm publication approval, the proposed date/time, final voice listening acceptance and the current AI use control under Attributes (or its current equivalent). Assess the intended realistic AI narration separately from the schematic animation; a description statement does not replace required upload disclosure. See platform-policy-review.md for freshly retrieved official-source evidence. Do not infer monetization approval from technical QA or licensing alone.
