# How Spring Dependency Injection Works — timed storyboard

Seven scenes, 1080×1920 vertical, 60 FPS. Navy background, white text, cyan/purple/Spring-green accents and subtle iSLDevs branding. Important content stays inside X=90..990, Y=250..1520. The actual local Kokoro narration timeline is 35.649833 seconds; frame rounding gives a 35.650000-second MP4. The exact cover occupies 00:00–00:01 without a fade or overlaid caption, with narration starting immediately.

The times below are actual synthesized scene boundaries from source/timing.json. The implemented drawing sequence below follows source/animation/render.py; final encoded-file and mobile-readability acceptance is recorded separately in verification-report.md.

| Scene and actual time | Spoken idea | Purposeful progressive visual | Captions |
| --- | --- | --- | --- |
| Hook · 0.000000–2.373917 | How does a repository reach your service? | Exact Spring DI cover, then a reference/connection prompt between Repo and OrderService. Keep the cover still for the first second. | The separate SRT begins at zero; the cover itself supplies the opening question. |
| Discover and register · 2.373917–7.382792 | Configured scanning finds annotated classes and registers bean definitions. | Show “App: register Config.class, then refresh,” followed by @Configuration and @ComponentScan("lesson.di"). A scan reveals @Repository Repo and @Service OrderService class metadata, then registers their definitions. Definitions are distinct from runtime objects. | Configured scan; annotated classes; bean definitions. |
| Resolve · 7.382792–12.970750 | The constructor needs a repository; Spring resolves its type. | Show OrderService(Repo repo). Highlight Repo in the parameter and match it to the unique Repo definition in the registry. | Constructor requirement, then type resolution. |
| Inject · 12.970750–18.441708 | Spring creates Repo and passes its reference into the constructor. | Create the Repo object, then move its reference into OrderService's constructor to assemble the ready graph. The service does not construct its repository. | Creation, then the supplied reference. |
| Verify and use · 18.441708–25.153958 | The Java run confirms identity before application use. | Show getBean(OrderService.class), the already-wired Repo/OrderService graph and actual Java excerpt “same Repo bean: true.” Grow the application request and returned-reference arrows, then reveal “application result: ready.” Both lines are present in the actual saved run. | Actual Java confirmation; application use after wiring. |
| Complete flow · 25.153958–34.209083 | Scan, register, resolve, inject, use; Spring supplies dependencies. | Stack the actual Config.class/@ComponentScan("lesson.di") input, @Repository Repo and @Service OrderService definitions, the OrderService(Repo repo) type requirement, and the injected Repo→OrderService runtime graph. Only then reveal an App-use endpoint. The complete mechanism is built before the dedicated two-second reading hold. | Five flow verbs and the construction-ownership takeaway. |
| Thanks · 34.209083–35.649833 | Thanks for watching. | Separate navy Thanks card with one gentle underline reveal. Keep the same original audio bed continuous and fade its closing tail. | The card supplies the spoken closing words on screen; retain the synchronized separate SRT cue. |

## Recap reading time

Scene 6 speech ends at **32.209083 s**. Hold the completed overview from **32.209083 to 34.209083 s**, exactly two seconds, then show the Thanks card. This is not a hold at the end of the file: Thanks follows it. The first five scenes explain discovery, parameter resolution, constructor injection and verification before application use.

## Verification and limits

Inspect the actual encoded graph for arrow direction, readable code and safe bounds. Source previews alone are insufficient. Default singleton startup timing and unique Repo matching are properties of this example. Spring manages the registered beans; the video does not claim it constructs every Java object. Technical/prosody checks do not certify subjective voice naturalness; no unperformed listening review is claimed.
