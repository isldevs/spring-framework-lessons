# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Context smoke test
- Publish date: 2026-11-22 (Sunday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared metadata only. No upload, scheduling or publication has been performed.

## Title

Spring Context Smoke Test: What Does It Prove?

## Description and hashtags

A Spring context smoke test checks the configuration and wiring you chose to assert.

This example uses @SpringJUnitConfig(Config.class) to load a Spring test context. Config creates a Repo bean and supplies it to OrderService through its constructor. The demo beans use Spring's default singleton scope.

The JUnit test retrieves OrderService and Repo with getBean, checks that the service exists, and uses assertSame to confirm that service.repository() is the context's Repo instance. Object identity matters here; matching values alone do not establish that wiring relationship.

A pass covers this selected configuration, required bean lookup and dependency assertion. Order behavior and other application features need separate tests. Lazy beans or unrelated configuration are not automatically covered by these assertions.

Spring's test framework can cache compatible contexts; this example does not claim that every test method gets a newly created context.

Official Spring references:
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/test/context/junit/jupiter/SpringJUnitConfig.html
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/test/context/junit/jupiter/SpringExtension.html

#SpringTesting #SpringFramework #JUnit5 #ApplicationContext #Java #Shorts #iSLDevs

## Tags (comma-separated)

context smoke test, Spring testing, Spring Framework, SpringJUnitConfig, JUnit 5, Spring TestContext, ApplicationContext, getBean, constructor injection, assertSame, Java, iSLDevs

## Pinned comment

A passing smoke test says that this selected context loaded and these assertions passed.

assertSame checks whether the service holds the exact Repo instance retrieved from the context. It does not compare only values.

Which business behavior would you test separately?
