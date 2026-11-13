# What Is Spring IoC?

Original English narration for iSLDevs. Six scene segments; pronounce `getBean` as “get bean.” Delivery target: a younger to middle-aged adult male English style, speaking smoothly as a person explaining the idea to a colleague. Keep a warm, clear tone, connected phrases, natural sentence endings, and short pauses between ideas. Voice age is a requested impression, not a verified speaker age. Do not speak scene labels or code punctuation.

1. Who creates your Java objects?

2. Without Spring, your code creates a repository, then passes it into a service.

3. With Spring, you register bean definitions. The container uses them to create managed objects and wire their dependencies.

4. Here, the service bean asks for a repository. Spring supplies that bean.

5. Your application calls `getBean` to request the ready service. In our Java run, its repository is the same bean from the container.

6. That’s inversion of control. Construction and wiring move to Spring, for managed beans, not every Java object.

Local voice configuration: Kokoro v1.0, 80% `am_puck` + 20% `am_fenrir`, speed 1.02. Both source voice styles are identified as male in the official voice table. No pitch shifting is used. This configuration targets the requested delivery; it is not a claim of completed perceptual acceptance.

## Delivery notes

- Give “Who creates” a curious lift, then settle into a calm, conversational explanation. Avoid a forceful announcer voice or exaggerated emphasis.
- Synthesize each complete scene as one utterance so sentence-level prosody can flow across clauses. Use brief pauses between scenes; avoid stitching separately spoken fragments in the middle of a sentence.
- Keep the approved animation design. Re-time scene boundaries, captions, reference movement, and audio cues to this revised narration.
- Separate “bean definitions” from the runtime objects in the explanation and visuals.
- In the example, the repository is a constructor dependency of the service; the `@Bean` method receives the repository bean and passes it to the constructor.
- The application’s `getBean` call retrieves a managed service. In this example, default singleton beans are created when the annotation context starts; the request does not imply a fresh construction on every call.
- Emphasize “managed beans” in the last line. Spring does not create every Java object.
- Match captions and scene boundaries to the final generated narration, rather than forcing the voice into estimated durations.
