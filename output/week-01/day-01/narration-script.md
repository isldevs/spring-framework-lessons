# What Is Spring IoC?

Original English narration for iSLDevs. Seven scene segments; pronounce `getBean` as “get bean.” Delivery target: a younger to middle-aged adult male English style, speaking smoothly as a person explaining the idea to a colleague. Keep a warm, clear tone, connected phrases, natural sentence endings, and short pauses between ideas. Voice age is a requested impression, not a verified speaker age. Do not speak scene labels or code punctuation.

1. Who creates your Java objects?

2. Without Spring, your code creates a repository, then passes it into a service.

3. With Spring, you register bean definitions. The container uses them to create managed objects and wire their dependencies.

4. Here, the service bean asks for a repository. Spring supplies that bean.

5. Your application calls `getBean` to request the ready service. In our Java run, its repository is the same bean from the container.

6. Your app starts Spring with Config. Spring calls Config’s bean methods, creates Repo, and wires Service. Your app retrieves the ready service. Managed beans only.

7. Thanks for watching.

Local voice configuration: Kokoro v1.0, 80% `am_puck` + 20% `am_fenrir`, speed 1.02. Both source voice styles are identified as male in the official voice table. No pitch shifting is used. This configuration targets the requested delivery; it is not a claim of completed perceptual acceptance.

## Delivery notes

- Give “Who creates” a curious lift, then settle into a calm, conversational explanation. Avoid a forceful announcer voice or exaggerated emphasis.
- Synthesize each complete scene as one utterance so sentence-level prosody can flow across clauses. Use brief pauses between scenes; avoid stitching separately spoken fragments in the middle of a sentence.
- Retain the approved cover and first five explanatory scenes. Make the recap concrete: the application starts Spring with `Config.class`; Spring reads the configuration and calls its `@Bean` factory methods, creates Repo and wires Service, then returns the ready service on application lookup. Hold the completed overview for at least two seconds, then show the brief “Thanks for watching” card.
- The user permits up to 45 seconds where needed for clarity. Let narration and diagram reading time determine pacing rather than compressing the explanation into a shorter duration. Re-time captions, reference movement, and audio cues to the actual speech.
- Separate “bean definitions” from the runtime objects in the explanation and visuals.
- Config is a Java configuration class. The application passes `Config.class` to `new AnnotationConfigApplicationContext(Config.class)`; Spring processes the class’s `@Bean` factory methods. Show this startup step before the creation/wiring arrows.
- The `repo()` factory returns a Repo instance. Spring resolves the `Repo repo` factory parameter before calling `service(repo)`, whose constructor call returns the Service instance. This is distinct from the later application `getBean` lookup.
- In the example, the repository is a constructor dependency of the service; the `@Bean` method receives the repository bean and passes it to the constructor.
- The application’s `getBean` call retrieves a managed service. In this example, default singleton beans are created when the annotation context starts; the request does not imply a fresh construction on every call.
- Emphasize “managed beans” at the end of the recap. Spring does not create every Java object. Speak “Thanks for watching” only after the recap reading hold, with the matching end card visible.
- Match captions and scene boundaries to the final generated narration, rather than forcing the voice into estimated durations.
