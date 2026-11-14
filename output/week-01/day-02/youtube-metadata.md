# YouTube Shorts metadata

## Title

How Spring Dependency Injection Works

## Description with hashtags

How does Spring get a repository into your service?

Follow a configured component scan, bean-definition registration, a constructor parameter matched by type, and the repository reference passed into OrderService before application use.

This Java example has one Repo bean and one OrderService constructor. Spring supplies the same repository bean from the context; that single constructor does not need @Autowired.

Official Spring references:
https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html
https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired.html

iSLDevs — Java and Spring, made visual.

#SpringFramework #DependencyInjection #Java #SpringDI #Shorts #iSLDevs

## Tags — comma-separated

Spring dependency injection, Spring DI, constructor injection, Spring Framework, Java, component scanning, ComponentScan, Spring beans, Repository, Service, Autowired, dependency graph, iSLDevs

## Pinned comment

Scanning must be configured. Here, one Repo bean matches the single OrderService constructor's parameter, so Spring can inject it without @Autowired on that constructor.

Multiple matching candidates need disambiguation, for example @Qualifier or @Primary. Which should we visualize next?
