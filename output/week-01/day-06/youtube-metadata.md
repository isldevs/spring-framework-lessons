# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Multiple contexts
- Publish date: 2026-11-21 (Saturday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared metadata only. No upload, scheduling or publication has been performed.

## Title

Spring Contexts: Who Can See Which Beans?

## Description and hashtags

Two ApplicationContext instances in one Java application do not automatically share beans.

Context A registers alpha; independent context B registers beta. A can retrieve alpha by name, but its lookup cannot find beta in B.

In a fresh parent-child hierarchy, setParent(parent) runs before the child is refreshed. The child checks its own registry first. If a named bean is absent locally, lookup can continue in the parent. The returned shared bean is the parent's existing instance, not a copy in the child.

The parent does not search its children for a bean. The runnable Java example and tests verify independent isolation, upward fallback and missing reverse visibility.

This lesson demonstrates named getBean lookups. A child's local bean with the same name can hide a parent bean for that child's lookup. APIs that list beans have their own hierarchy rules.

Official Spring references:
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/BeanFactory.html
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/HierarchicalBeanFactory.html

#ApplicationContext #SpringFramework #SpringIoC #Java #SpringBeans #Shorts #iSLDevs

## Tags (comma-separated)

multiple Spring contexts, ApplicationContext, Spring Framework, Spring IoC, parent child context, bean visibility, getBean, HierarchicalBeanFactory, containsLocalBean, Java, Spring beans, iSLDevs

## Pinned comment

A named lookup starts in the child and can fall back to its parent. A parent lookup does not search down into child contexts.

If the child registers its own bean named shared, that local name hides the parent's shared bean for the child's lookup. The parent bean stays unchanged.

Which beans would you put in a parent context?
