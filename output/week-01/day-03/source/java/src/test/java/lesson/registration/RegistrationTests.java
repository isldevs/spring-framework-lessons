package lesson.registration;

import java.util.concurrent.atomic.AtomicBoolean;
import lesson.scan.Worker;
import lesson.outside.Outside;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.SpringVersion;
import org.springframework.stereotype.Component;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(OrderAnnotation.class)
class RegistrationTests {
    @Test @Order(1)
    void aPlainClasspathClassHasNoDefinitionOrManagedInstance() {
        Trace.clear();
        assertEquals("6.2.11", SpringVersion.getVersion());
        assertFalse(Client.class.isAnnotationPresent(Component.class));
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.refresh();
            assertTrue(ctx.isActive());
            assertFalse(ctx.containsBeanDefinition("client"));
            assertFalse(ctx.getBeanFactory().containsSingleton("client"));
            assertThrows(NoSuchBeanDefinitionException.class, () -> ctx.getBean(Client.class));
            assertEquals(0, Trace.clients);
            System.out.println("plain class missing: true");
        }
    }

    @Test @Order(2)
    void registeredConfigurationAddsAFactoryDefinitionAndRetrievableSingleton() {
        Trace.clear();
        AtomicBoolean observedDefinition = new AtomicBoolean();
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(FactoryConfig.class);
            assertTrue(ctx.containsBeanDefinition("factoryConfig"));
            assertFalse(ctx.containsBeanDefinition("client"));
            assertEquals(0, Trace.clients);
            ctx.addBeanFactoryPostProcessor(factory -> {
                BeanDefinition definition = factory.getBeanDefinition("client");
                assertEquals("factoryConfig", definition.getFactoryBeanName());
                assertEquals("client", definition.getFactoryMethodName());
                assertTrue(definition.isSingleton());
                assertFalse(factory.containsSingleton("client"));
                assertEquals(0, Trace.clients);
                assertEquals(0, Trace.factoryCalls);
                observedDefinition.set(true);
                System.out.println("@Bean definition before instance: true");
            });
            ctx.refresh();
            assertTrue(observedDefinition.get());
            assertTrue(ctx.containsBeanDefinition("client"));
            Client first = ctx.getBean(Client.class);
            assertSame(first, ctx.getBean("client"));
            assertSame(first, ctx.getBean(Client.class));
            assertEquals("explicit", first.name());
            assertEquals(1, ctx.getBeansOfType(Client.class).size());
            assertEquals(1, Trace.clients);
            assertEquals(1, Trace.factoryCalls);
            System.out.println("@Bean retrieved: true");
        }
    }

    @Test @Order(3)
    void configuredScanRegistersItsComponentAndExcludesAnAnnotatedOutsideClass() {
        Trace.clear();
        AtomicBoolean observedDefinition = new AtomicBoolean();
        assertTrue(Worker.class.isAnnotationPresent(Component.class));
        assertTrue(Outside.class.isAnnotationPresent(Component.class));
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(ScanConfig.class);
            ctx.addBeanFactoryPostProcessor(factory -> {
                BeanDefinition definition = factory.getBeanDefinition("worker");
                assertEquals("lesson.scan.Worker", definition.getBeanClassName());
                assertNull(definition.getFactoryMethodName());
                assertTrue(definition.isSingleton());
                assertFalse(factory.containsSingleton("worker"));
                assertEquals(0, Trace.workers);
                assertFalse(factory.containsBeanDefinition("outside"));
                observedDefinition.set(true);
                System.out.println("scan definition before instance: true");
            });
            ctx.refresh();
            assertTrue(observedDefinition.get());
            Worker first = ctx.getBean(Worker.class);
            assertSame(first, ctx.getBean("worker"));
            assertSame(first, ctx.getBean(Worker.class));
            assertEquals("scanned", first.name());
            assertEquals(1, Trace.workers);
            assertFalse(ctx.containsBeanDefinition("client"));
            assertFalse(ctx.containsBeanDefinition("outside"));
            assertThrows(NoSuchBeanDefinitionException.class, () -> ctx.getBean(Outside.class));
            assertEquals(0, Trace.outsiders);
            System.out.println("scan retrieved: true");
            System.out.println("outside scan missing: true");
        }
    }
}
