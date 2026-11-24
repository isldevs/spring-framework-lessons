# Actual Spring multiple-context example

This minimal project runs real **Spring Framework 6.2.11**. It compares two independent `AnnotationConfigApplicationContext` instances with a fresh parent/child pair. All illustrated lookups select by **bean name**; this is not a claim that every enumeration or type-based API traverses the hierarchy identically.

## Reproduce

From the lesson directory:

```sh
bash source/java/run.sh
```

Requirements: Python 3 and a Java 17-or-newer runtime. The actual run used OpenJDK **21.0.13**. Pinned Eclipse ECJ **3.40.0** compiles Java 17-target main and test classes, so installed `javac` and Maven are unnecessary. Spring Boot is not used.

Ten pinned jars, their coordinates and SHA-256 hashes, and dependency notices are retained in `lib/`, `dependency-sources.json`, `dependencies.sha256` and `licenses/`. The dependency manifest is checked before compilation. `fetch-dependencies.py` can reproduce the downloads from Maven Central, verify published checksums and extract notices. It was also executed for this lesson.

`verify.py` captures exact commands, exit codes, stdout/stderr, runtime version, source hashes and JUnit XML in `../evidence/java-*`. `fetch-docs.py` retrieves the five official versioned API pages used to check the explanation; raw HTML/text, HTTP results, response hashes and supported excerpts are retained there too.

## Mechanism shown

Independent contexts have separate bean factories and no configured parent:

```java
try (var a = new AnnotationConfigApplicationContext(AConfig.class);
     var b = new AnnotationConfigApplicationContext(BConfig.class)) {
    a.getBean("alpha", Item.class); // A's local bean
    b.getBean("beta", Item.class);  // B's local bean
    // a.getBean("beta") throws NoSuchBeanDefinitionException.
}
```

The hierarchy uses **fresh** contexts. The parent is configured before the child is refreshed; the independent A/B contexts are not reparented while running.

```java
try (var parent = new AnnotationConfigApplicationContext(ParentConfig.class)) {
    try (var child = new AnnotationConfigApplicationContext()) {
        child.setParent(parent);
        child.register(ChildConfig.class);
        child.refresh();
        Item shared = child.getBean("shared", Item.class);
        // shared == parent.getBean("shared"): true
        // child.containsLocalBean("shared"): false
        // parent.getBean("local") throws NoSuchBeanDefinitionException.
    }
}
```

The parent contains the default-singleton `shared` bean; the child contains `local`. The child checks its local factory first and can delegate an absent bean name to its parent. It receives the **same parent-owned instance reference**, not a copied bean or copied definition. The parent has no corresponding child lookup fallback. An explicit local bean with the same name would hide the parent bean for that named lookup; the fourth test verifies this qualification separately.

The child closes before the parent. An assertion confirms that closing the child does not close its parent in this example. The small diagram shows the selected lesson beans; real contexts also contain configuration and framework infrastructure definitions.

## Four actual tests

1. Independent contexts have different bean factories and no parent; each resolves only its local example bean. Both cross-context name lookups throw `NoSuchBeanDefinitionException`, while both contexts remain active.
2. A child resolves its own `local` bean and obtains the same `shared` instance as its parent. `containsBean("shared")` is true while `containsLocalBean("shared")` and `containsBeanDefinition("shared")` are false. `getBeansOfType(Item.class)` enumerates only each context's local beans. The parent remains active after the child closes.
3. A parent cannot retrieve the child's `local` bean through its own named `getBean` lookup; the actual exception reports the missing name.
4. A child-local `shared` bean shadows the parent's `shared` for named lookup, without replacing or mutating the parent's bean.

Actual result: **4 tests found, 4 started, 4 successful, 0 failed**. Main compilation, test compilation, JUnit and standalone application all exited **0**, with empty stderr.

## Actual application output

```text
A alpha: alpha
B beta: beta
A beta: missing
A beta exception: NoSuchBeanDefinitionException
B alpha: missing
B alpha exception: NoSuchBeanDefinitionException
child shared: shared
child shared same: true
child owns shared: false
child local: local
parent local: missing
parent local exception: NoSuchBeanDefinitionException
parent active after child close: true
```

The `missing` labels are printed only after catching and checking the actual exception. No startup failure, benchmark or timing claim is implied.

## Official references

- [BeanFactory 6.2.11](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/BeanFactory.html): parent fallback and local-name precedence.
- [HierarchicalBeanFactory 6.2.11](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/HierarchicalBeanFactory.html): parent access and local-only containment.
- [ListableBeanFactory 6.2.11](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/beans/factory/ListableBeanFactory.html): local enumeration boundaries.
- [ConfigurableApplicationContext 6.2.11](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/ConfigurableApplicationContext.html): `setParent` and lifecycle API.
- [AnnotationConfigApplicationContext 6.2.11](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/context/annotation/AnnotationConfigApplicationContext.html): explicit registration/refresh and convenient configuration constructors.
