# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: ApplicationContext
- Publish date: 2026-11-17 (Tuesday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared metadata only. No upload, scheduling or publication has been performed.

## Title

What's Inside ApplicationContext?

## Description and hashtags

ApplicationContext holds more than objects. Bean definitions describe what to build; managed instances are the actual objects.

Follow an AnnotationConfigApplicationContext as it registers configuration, refreshes, creates the demo's non-lazy singleton beans and returns an already wired service through getBean.

The context also dispatches an application event and runs managed bean cleanup when closed. The runnable example checks bean identity, one handled event and cleanup. A separate lazy-bean test shows that a definition can exist before its object is created.

Official Spring references:
https://docs.spring.io/spring-framework/6.2/reference/core/beans/basics.html
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/annotation/AnnotationConfigApplicationContext.html

#ApplicationContext #SpringFramework #SpringIoC #Java #DependencyInjection #Shorts #iSLDevs

## Tags (comma-separated)

ApplicationContext, Spring Framework, Spring IoC, bean definitions, managed beans, singleton beans, getBean, AnnotationConfigApplicationContext, Spring lifecycle, application events, Java, iSLDevs

## Pinned comment

A bean definition describes an object; it is not the object itself. This example uses default non-lazy singletons, so refresh creates them before getBean. Lazy beans behave differently—the separate test covers that distinction.

Which container service should we animate next: events, resources or message lookup?
