# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Constructor injection
- Publish date: 2026-11-23 (Monday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared files only. No upload, scheduling or publication has been performed. Manual approval is required.

## Title

No @Autowired? Spring Still Wires This Service

## Description and hashtags

A Spring-managed class with a single constructor can use constructor injection without @Autowired.

OrderService requests PaymentGateway through its constructor. Config imports OrderService and DemoPaymentGateway, so this context has one matching gateway candidate. Spring resolves that dependency and supplies its reference to the constructor.

Two real JUnit tests verify the single unannotated constructor, the injected gateway's identity, service execution returning demo-paid:2500, and a manual-construction control. The gateway is an in-memory demo; no real payment is processed.

With new OrderService(gateway), you still provide the constructor argument yourself. Spring does not automatically wire arbitrary objects created with new.

Verified with Spring Framework 6.2.11 and JUnit 5.12.2. The single-constructor annotation rule has applied since Spring 4.3.

Narration is AI-generated.

Official Spring references:
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html
https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired.html

#ConstructorInjection #SpringFramework #DependencyInjection #Java #Autowired #Shorts #iSLDevs

## Tags (comma-separated)

constructor injection, Spring Framework, dependency injection, Autowired, single constructor, OrderService, PaymentGateway, Spring beans, Java, Spring IoC, JUnit 5, iSLDevs

## Pinned comment

The key conditions here are a Spring-managed service, one constructor, and one matching PaymentGateway candidate.

For a plain Java test, new OrderService(fakeGateway) makes the dependency explicit without starting Spring.

What behavior would your fake gateway return?

## Manual thumbnail selection

Where the YouTube app's Shorts upload/edit flow offers thumbnail editing, open its thumbnail/frame selector and choose the recognizable opening composition from the first second. Confirm that “Spring Injection”, the blue “No @Autowired?” highlight and “It still works.” remain readable in the displayed crop. Use cover.png only if that upload flow supports selecting a separate image. Controls differ by app/version; neither automatic selection nor availability is guaranteed.

## Manual upload confirmation

Confirm publication approval, the proposed date/time, final voice listening acceptance and the current AI use control under Attributes (or its current equivalent). Assess the intended realistic AI narration separately from the schematic animation; a description statement does not replace required upload disclosure. See platform-policy-review.md for official-source evidence and the distinction between this technical animation and realistic synthetic content. Do not infer monetization approval from technical QA or licensing alone.
