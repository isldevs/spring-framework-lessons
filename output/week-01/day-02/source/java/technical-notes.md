# ApplicationContext: actual runtime and animation boundaries

The production example intentionally uses manual lifecycle calls, not the convenience constructor taking `Config.class`. Its no-arg context must be registered and refreshed explicitly. The API's configuration-taking constructor would register and refresh automatically, which would conceal the distinction this lesson teaches.

The postprocessor observation is after `ConfigurationClassPostProcessor` has registered the `@Bean` definitions, but before ordinary Repo and Service singleton creation. The observation checks definition existence, absence from the singleton registry, zero application constructors and then the subsequent construction order. This is a real lifecycle observation, not an invented list of definitions or a timing benchmark.

`Service` is both a dependency consumer and a narrowly typed event listener to keep the project minimal. It also implements the managed singleton destruction contract. This combines lookup, event publication and cleanup without adding another application bean and does not suggest every production service should implement all three interfaces. Resource loading and message resolution are additional ApplicationContext services supported by the official docs; this example does not claim to have tested those extra services.

The root-level narration/visual timeline has explanatory durations, not Java runtime measurements. Internal infrastructure definitions are deliberately omitted from the small demo diagram. `Config` itself is a managed configuration bean as well as the source of the two illustrated `@Bean` definitions; the video focuses on the two named application beans rather than pretending the full context contains only them.

No Spring Boot startup, HTTP server, external database, remote event broker or performance benchmark is involved. Tests and app execute locally using actual Spring Framework6.2.11.
