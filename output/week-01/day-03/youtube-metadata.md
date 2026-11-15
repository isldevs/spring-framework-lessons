# YouTube Shorts metadata

## Title

Constructor Injection in Spring Boot

## Description and hashtags

OrderService needs a PaymentGateway. How does Spring Boot supply it?

Follow a PaymentGateway reference through the OrderService constructor into a final field. Boot starts Spring, scans the application's package, and resolves one matching DemoGateway component.

The example checks that OrderService receives the managed gateway bean. A separate service test supplies a recording fake through the same constructor.

Demo only: payment approvals are simulated. No real transaction or payment API is called.

Official Spring references:
https://docs.spring.io/spring-boot/reference/using/spring-beans-and-dependency-injection.html
https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired.html

iSLDevs — Java and Spring, made visual.

#SpringBoot #ConstructorInjection #DependencyInjection #Java #Shorts #iSLDevs

## Tags (comma-separated)

constructor injection, Spring Boot, Spring dependency injection, OrderService, PaymentGateway, Java, final field, single constructor, Autowired, unit testing, fake gateway, dependency graph, iSLDevs

## Pinned comment

One constructor, one matching PaymentGateway bean: this constructor does not need @Autowired.

DemoGateway simulates approval locally. The recording fake is supplied manually only in the separate service test.

Which would help next: testing constructor injection or handling multiple matching gateway beans?
