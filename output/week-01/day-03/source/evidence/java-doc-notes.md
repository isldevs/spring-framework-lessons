# Official documentation verification — Bean registration

Eight official Spring pages were actually retrieved with HTTP200. API references are pinned to Spring Framework6.2.11; narrative references use the6.2 documentation branch. `java-doc-official-documentation.json` retains requested/resolved URLs, status, HTML SHA-256 and verbatim excerpts; original HTML and extracted text are retained. `java-doc-fetch.py` reproduces those requests.

The docs establish that `@Bean` methods describe factories and register definitions when the enclosing configuration is processed; a configuration class is registered and refreshed through AnnotationConfigApplicationContext. `@Component` marks a candidate for discovery, while configured component scanning chooses the package boundary and registers detected definitions. The classpath is not an unconditional registry of every Java class. The actual negative/positive examples and package-boundary results must be verified by the accompanying Java tests, rather than inferred as fabricated output from documentation.

The lesson demonstrates two valid registration paths, not an exhaustive list. Other supported mechanisms include direct programmatic registration and XML. A component annotation can also be used with explicitly registered component classes; the missing-outside-scan example is scoped to a context configured to scan only `lesson.scan`, with no other registration path for that class. Bean definition registration is distinct from object construction. Default non-lazy singleton examples may be constructed during refresh; this does not generalize to every scope or lazy bean.

Approved publishing references, both retrieved successfully:

- https://docs.spring.io/spring-framework/reference/6.2/core/beans/java/bean-annotation.html
- https://docs.spring.io/spring-framework/reference/6.2/core/beans/classpath-scanning.html

No Java compilation/test result or auditory review is established by these documentation requests.
