# Bean naming — exact verification scope

The public lesson topic is Bean naming. It compares an explicitly assigned bean ID with type-based lookup; it does not conflate names with qualifier annotations or claim that distinct names universally resolve type ambiguity.

AlphaConfig has `@Bean("alpha") Client client()`. The test observes the BeanDefinition under alpha and its factory method metadata client. It checks that `containsBean("client")` is false. This is the explicit-name case; no alias/default-component-naming behavior is inferred.

In the single-Client context, String-only lookup, String+Class lookup and Class-only lookup all return the same managed singleton. In the two-Client context, alpha and beta select different instances by name, while the unprioritized Client-only lookup throws NoUniqueBeanDefinitionException with two candidates. Both definitions have primary=false, and Client has no priority annotation. The retained default singleton behavior is not generalized to every scope or lazy arrangement.

String+Class means “find this named bean and ensure its type matches.” It does not mean “choose any bean of that type.” The wrong-required-type test captures BeanNotOfRequiredTypeException and checks selected name, actual type and required type.

The separate @Qualifier("beta") consumer test deliberately combines both Client beans with one constructor injection point. The parameter receives beta, but an unrelated BeanFactory.getBean(Client.class) query stays ambiguous. This proves the distinction rather than relying on a slogan about qualifiers. Bean names can participate in qualifier fallback matching; that fact does not turn the two API mechanisms into identical operations.

The standalone app catches only the expected ambiguity and fails assertions if it does not occur. Actual exception message text and all command outputs are preserved. Its process exit0 denotes successful expected-behavior verification, not absence of the intentionally demonstrated exception.

The two public runtime scenarios create separate fresh contexts and close each. New declarations are not registered by attempting a second refresh on the same GenericApplicationContext. Animation timestamps are explanatory edits, not Java execution measurements or lookup benchmarks.

The actual test run uses Spring6.2.11, ECJ3.40.0 targeting Java17, JDK21.0.13 and JUnit Jupiter5.12.2/platform1.12.2. There are four successful tests and no failed/skipped tests. No Maven, javac or Boot execution is claimed. Dependency checks, source hashes and all licenses/notices are retained for reproduction.
