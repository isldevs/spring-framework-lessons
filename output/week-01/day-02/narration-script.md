# How Spring Dependency Injection Works

Original English narration for iSLDevs. Seven coherent scene utterances. The local male Kokoro style targets a younger-to-middle adult giving a smooth explanation. Delivery is not considered perceptually accepted until actual listening review is possible.

1. How does a repository reach your service?

2. Configured scanning finds annotated classes and registers bean definitions.

3. A single constructor needs a repository. Spring resolves that parameter by type.

4. Spring creates the repository, then passes its reference into the service constructor.

5. Our Java run confirms the same repository bean. Only then does the application use the service.

6. Scan, register, resolve, inject, then use. Spring supplies dependencies; your service doesn’t construct them.

7. Thanks for watching.

## Delivery and technical notes

- Explain the sequence conversationally. Preserve the distinction between registering bean definitions and constructing bean instances.
- Repo is the repository bean; OrderService is the dependent service. The only OrderService constructor takes Repo, so no @Autowired annotation is necessary on that constructor.
- Scanning is explicitly configured for the lesson.di package by Config's @ComponentScan annotation. Spring does not discover arbitrary classes in every package.
- This example has one matching Repo bean. Multiple candidates can require @Qualifier or @Primary; the video does not claim type alone always disambiguates them.
- The actual example uses default, non-lazy singleton beans: startup assembles the graph before the application requests and uses the ready service. Do not generalize eager creation timing to every bean scope or lazy bean.
- Hold the completed recap for two seconds before the spoken Thanks card. Do not speak internal scene labels or schedule identifiers.
- No public day, week, lesson or episode number is included.
