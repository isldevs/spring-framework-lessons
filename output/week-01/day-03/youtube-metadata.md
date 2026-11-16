# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Bean registration
- Publish date: 2026-11-18 (Wednesday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared metadata only. No upload, scheduling or publication has been performed.

## Title

Why Isn't This Class a Spring Bean?

## Description and hashtags

Why is a plain Java class missing from Spring?

Compare two bean registration paths: an @Bean factory method in registered configuration, and an @Component class found by component scanning.

Follow each path into Spring's bean definitions and then retrieve the managed bean with getBean. The example also checks that an annotated class outside the configured scan package stays unregistered.

The runnable Spring Framework tests check missing lookups, both successful registration paths and default singleton reuse.

Official Spring references:
https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html
https://docs.spring.io/spring-framework/reference/6.2/core/beans/classpath-scanning.html

#BeanRegistration #SpringFramework #SpringIoC #Java #Shorts #iSLDevs

## Tags (comma-separated)

bean registration, Spring Framework, Spring IoC, Bean, Component, ComponentScan, Java, bean definition, getBean, Spring configuration, singleton beans, iSLDevs

## Pinned comment

The configured scan must cover the class's package. Merely adding @Component does not activate scanning.

For the factory path, the configuration class must also be registered. The demo tests those steps in separate contexts.

Which registration path do you use most: @Bean or component scanning?
