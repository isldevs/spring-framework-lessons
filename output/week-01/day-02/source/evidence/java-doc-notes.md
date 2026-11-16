# Official Spring documentation review

The accompanying retrieval script actually fetched ten official pages, all HTTP200. HTML, extracted text, resolved URLs and SHA-256 hashes are retained. API pages are fixed to Spring Framework6.2.11; reference pages are on the6.2 documentation branch. The claims JSON contains direct excerpts rather than invented quotations.

- The no-arg AnnotationConfigApplicationContext must be populated and refreshed explicitly. Registering Config.class alone does not mean its @Bean instances already exist. Configuration-class processing during refresh adds the @Bean definitions.
- A BeanDefinition records creation metadata. It is distinct from the bean instance. A programmatically registered BeanFactoryPostProcessor can inspect definitions before ordinary bean construction without calling getBean.
- Default ApplicationContext singleton creation is eager at initialization. Do not claim all beans always exist immediately: lazy singletons and other scopes have different timing. A lazy bean required by an eager singleton can still be instantiated during startup.
- ApplicationContext supplies bean lookup and container services including event publishing, resources and message resolution. The compact lesson demonstrates event publishing and managed destruction; it does not need to imply these are its only services.
- EventPublisher publication generally hands off to an event multicaster; synchronous/immediate handling is not an interface-level promise. An observed default synchronous listener in this example is a property of the demonstrated configuration.
- AbstractApplicationContext.close destroys beans in its bean factory. DisposableBean singletons receive destroy callbacks at shutdown. Do not generalize container-managed destruction callbacks to every scope: prototype lifecycle cleanup is a separate concern.

The official wording “destroying all beans” should be read alongside scope/lifecycle semantics; the executable example verifies its own ordinary singleton. No version-specific runtime behavior is inferred from unretrieved pages.
