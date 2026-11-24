# Multiple contexts: claim boundaries

The lesson demonstrates actual named bean lookup in Spring Framework 6.2.11. The `Item` value is a plain Java record used only to mark the returned bean. The same Java class is used in different contexts; loading that class does not make the contexts share registrations or instances.

Independent A/B contexts have separate `DefaultListableBeanFactory` instances and no parent. A registers alpha; B registers beta. Both local lookups succeed and both opposite-name lookups fail after successful startup. The lookup failures do not stop or destroy the contexts.

The parent/child example is a fresh pair. The application creates and refreshes ParentConfig, then creates an empty child, sets its parent, registers ChildConfig and refreshes the child. This does not demonstrate setting a new parent on a running context or refreshing a GenericApplicationContext twice.

For the illustrated name, local lookup comes first. If the local definition is absent, Spring's hierarchy can consult the parent. `child.getBean("shared", Item.class)` returns the same already-created default-singleton object as `parent.getBean("shared")`. It does not copy the parent definition or object into the child registry. `containsLocalBean` and `containsBeanDefinition` stay false for shared in the child.

The parent does not search down into this child by default. A parent lookup for local throws `NoSuchBeanDefinitionException`; no parent/child reverse-sharing mechanism is added by this example. A separate test verifies local same-name shadowing, so upward access should not be phrased as every child always receiving every parent bean.

Do not generalize the pictured named lookup to all APIs. In particular, ListableBeanFactory enumeration methods such as `getBeansOfType` are local to the current factory; ancestor-aware helper methods exist separately. This example intentionally uses explicit names to avoid conflating named fallback, type candidate selection and enumeration.

The objects shown in the lesson are selected application beans. Configuration-class beans and Spring infrastructure definitions are omitted from the diagram for readability. Registry and object/reference visuals are conceptual explanations of verified behavior, not heap snapshots or measured execution traces.

All exceptions and successful output are captured from the real run. No runtime speed/benchmark is asserted. Actual JDK21.0.13, ECJ3.40.0 Java17 target, JUnit Jupiter5.12.2 / console1.12.2 and Spring6.2.11 were used; Maven, javac and Spring Boot were not used.

Four substantive tests, application output, source hashes and five freshly fetched official versioned API pages support the claims. Raw evidence is in `../evidence/java-*`. The original example source is licensed by the adjacent LICENSE; third-party licenses/notices are in `licenses/`.
