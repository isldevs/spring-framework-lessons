package lesson.contexts;

import java.util.Set;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.SpringVersion;
import static org.junit.jupiter.api.Assertions.*;

class ContextsTests {
    @Test
    void independentContextsKeepSeparateRegistriesAndLookups() {
        try (var a = new AnnotationConfigApplicationContext(AConfig.class);
             var b = new AnnotationConfigApplicationContext(BConfig.class)) {
            assertEquals("6.2.11", SpringVersion.getVersion());
            assertNull(a.getParent());
            assertNull(b.getParent());
            assertNotSame(a.getBeanFactory(), b.getBeanFactory());
            assertEquals("alpha", a.getBean("alpha", Item.class).id());
            assertEquals("beta", b.getBean("beta", Item.class).id());
            assertTrue(a.containsBeanDefinition("alpha"));
            assertFalse(a.containsBeanDefinition("beta"));
            assertTrue(b.containsBeanDefinition("beta"));
            assertFalse(b.containsBeanDefinition("alpha"));
            assertEquals(Set.of("alpha"), a.getBeansOfType(Item.class).keySet());
            assertEquals(Set.of("beta"), b.getBeansOfType(Item.class).keySet());
            NoSuchBeanDefinitionException aFailure = assertThrows(NoSuchBeanDefinitionException.class,
                    () -> a.getBean("beta"));
            NoSuchBeanDefinitionException bFailure = assertThrows(NoSuchBeanDefinitionException.class,
                    () -> b.getBean("alpha"));
            assertEquals("beta", aFailure.getBeanName());
            assertEquals("alpha", bFailure.getBeanName());
            assertTrue(a.isActive());
            assertTrue(b.isActive());
            System.out.println("independent context isolation: passed");
        }
    }

    @Test
    void childFallsBackToSameParentBeanWithoutCopyingItsDefinition() {
        try (var parent = new AnnotationConfigApplicationContext(ParentConfig.class)) {
            try (var child = new AnnotationConfigApplicationContext()) {
                child.setParent(parent);
                child.register(ChildConfig.class);
                child.refresh();
                assertSame(parent, child.getParent());
                assertNotSame(parent.getBeanFactory(), child.getBeanFactory());
                assertEquals("local", child.getBean("local", Item.class).id());
                assertSame(parent.getBean("shared"), child.getBean("shared", Item.class));
                assertTrue(child.containsBean("shared"));
                assertFalse(child.containsLocalBean("shared"));
                assertFalse(child.containsBeanDefinition("shared"));
                assertTrue(child.containsLocalBean("local"));
                assertEquals(Set.of("local"), child.getBeansOfType(Item.class).keySet());
                assertEquals(Set.of("shared"), parent.getBeansOfType(Item.class).keySet());
                System.out.println("child parent fallback same instance: passed");
            }
            assertTrue(parent.isActive());
            assertEquals("shared", parent.getBean("shared", Item.class).id());
        }
    }

    @Test
    void parentCannotLookDownIntoChildByDefault() {
        try (var parent = new AnnotationConfigApplicationContext(ParentConfig.class)) {
            try (var child = new AnnotationConfigApplicationContext()) {
                child.setParent(parent);
                child.register(ChildConfig.class);
                child.refresh();
                assertTrue(child.containsLocalBean("local"));
                assertFalse(parent.containsBean("local"));
                assertFalse(parent.containsLocalBean("local"));
                NoSuchBeanDefinitionException failure = assertThrows(NoSuchBeanDefinitionException.class,
                        () -> parent.getBean("local", Item.class));
                assertEquals("local", failure.getBeanName());
                assertTrue(parent.isActive());
                assertTrue(child.isActive());
                System.out.println("parent cannot see child local bean: passed");
            }
        }
    }

    @Test
    void childSameNameShadowsParentForNamedLookup() {
        try (var parent = new AnnotationConfigApplicationContext(ParentConfig.class)) {
            try (var child = new AnnotationConfigApplicationContext()) {
                child.setParent(parent);
                child.register(ShadowConfig.class);
                child.refresh();
                Item parentShared = parent.getBean("shared", Item.class);
                Item childShared = child.getBean("shared", Item.class);
                assertEquals("shared", parentShared.id());
                assertEquals("child-shared", childShared.id());
                assertNotSame(parentShared, childShared);
                assertTrue(child.containsLocalBean("shared"));
                assertSame(parentShared, parent.getBean("shared"));
                System.out.println("local named bean shadows parent: passed");
            }
        }
    }

    @Configuration(proxyBeanMethods = false)
    static class ShadowConfig {
        @Bean("shared")
        Item shared() { return new Item("child-shared"); }
    }
}
