# YouTube Shorts metadata

## Publication plan

- Approved lesson topic: Bean naming
- Publish date: 2026-11-20 (Friday)
- Proposed publish time: 19:00 Asia/Phnom_Penh (UTC+07:00; 12:00 UTC)
- Publication status: Prepared metadata only. No upload, scheduling or publication has been performed.

## Title

Two Bean Names. One Ambiguous Type.

## Description and hashtags

An explicit @Bean name identifies a bean. It does not automatically make a type-only lookup unique.

Watch getBean("alpha") select by name, while getBean("alpha", Client.class) also checks the selected bean's type. With one Client, getBean(Client.class) returns the same object.

In a separate context, alpha and beta both match Client. With no primary or other selection preference in this demo, the type-only lookup throws NoUniqueBeanDefinitionException.

Named lookup and @Qualifier are different mechanisms: a name selects a lookup target; a qualifier guides injection candidate selection.

Official Spring references:
https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html
https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/BeanFactory.html

#BeanNaming #SpringFramework #SpringIoC #Java #DependencyInjection #Shorts #iSLDevs

## Tags (comma-separated)

bean naming, Spring Framework, Spring IoC, Bean, getBean, named lookup, type lookup, NoUniqueBeanDefinitionException, Primary, Qualifier, Java, iSLDevs

## Pinned comment

getBean("alpha", Client.class) selects the bean named alpha and checks its type.

@Qualifier is injection metadata. The separate qualifier test shows that injection can choose beta while this example's direct getBean(Client.class) lookup remains ambiguous.

Which lookup would you use here?
