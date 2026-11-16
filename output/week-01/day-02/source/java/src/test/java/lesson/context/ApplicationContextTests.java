package lesson.context;

import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.core.SpringVersion;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(OrderAnnotation.class)
class ApplicationContextTests {
    @Test @Order(1)
    void definitionsPrecedeSingletonsAndContextProvidesLookupEventsAndCleanup() {
        Trace.clear();
        AtomicBoolean observedDefinitions = new AtomicBoolean();
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
        try (ctx) {
            assertEquals("6.2.11", SpringVersion.getVersion());
            assertFalse(ctx.isActive());
            ctx.register(Config.class);
            // register adds Config metadata, not Repo or Service instances.
            assertTrue(ctx.containsBeanDefinition("config"));
            assertFalse(ctx.getBeanFactory().containsSingleton("config"));
            assertEquals(0, Trace.repos + Trace.services);
            ctx.addBeanFactoryPostProcessor(factory -> {
                assertTrue(factory.containsBeanDefinition("repo"));
                assertTrue(factory.containsBeanDefinition("service"));
                assertEquals("singleton", factory.getBeanDefinition("service").getScope().isEmpty()
                        ? "singleton" : factory.getBeanDefinition("service").getScope());
                assertEquals(0, Trace.repos + Trace.services);
                assertFalse(factory.containsSingleton("repo"));
                assertFalse(factory.containsSingleton("service"));
                Trace.record("definitions before instances: true");
                observedDefinitions.set(true);
            });
            ctx.refresh();
            Trace.record("context refreshed");
            assertTrue(observedDefinitions.get());
            assertTrue(ctx.isActive());
            assertEquals(1, Trace.repos);
            assertEquals(1, Trace.services);
            assertTrue(ctx.getBeanFactory().containsSingleton("repo"));
            assertTrue(ctx.getBeanFactory().containsSingleton("service"));
            Service service = ctx.getBean(Service.class);
            assertSame(service, ctx.getBean(Service.class));
            assertSame(ctx.getBean(Repo.class), service.repo());
            assertEquals("hello from repo", service.run());
            assertEquals(1, Trace.repos);
            assertEquals(1, Trace.services);
            List<String> order = Trace.snapshot();
            assertTrue(order.indexOf("definitions before instances: true") < order.indexOf("repo created"));
            assertTrue(order.indexOf("repo created") < order.indexOf("service created with repo"));
            assertTrue(order.indexOf("service created with repo") < order.indexOf("context refreshed"));
            Trace.record("same service: true");
            assertEquals(0, Trace.handled);
            ctx.publishEvent(new DemoEvent(ctx));
            assertEquals(1, Trace.handled);
            assertEquals(0, Trace.cleanup);
            Trace.record("events handled: " + Trace.handled);
        }
        assertFalse(ctx.isActive());
        assertEquals(1, Trace.cleanup);
        ctx.close(); // Closing again does not invoke the callback a second time.
        assertEquals(1, Trace.cleanup);
        Trace.record("cleanup called: true");
    }

    @Test @Order(2)
    void lazyDefinitionDoesNotImplyAnInstanceExistsAfterRefresh() {
        LazyConfig.created.set(0);
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(LazyConfig.class);
            ctx.refresh();
            assertTrue(ctx.containsBeanDefinition("lazyBean"));
            assertTrue(ctx.getBeanFactory().getBeanDefinition("lazyBean").isLazyInit());
            assertFalse(ctx.getBeanFactory().containsSingleton("lazyBean"));
            assertEquals(0, LazyConfig.created.get());
            LazyBean first = ctx.getBean(LazyBean.class);
            assertEquals(1, LazyConfig.created.get());
            assertTrue(ctx.getBeanFactory().containsSingleton("lazyBean"));
            assertSame(first, ctx.getBean(LazyBean.class));
            assertEquals(1, LazyConfig.created.get());
            System.out.println("lazy definition before instance: true");
        }
    }

    @Configuration(proxyBeanMethods = false)
    static class LazyConfig {
        static final AtomicInteger created = new AtomicInteger();
        @Bean @Lazy LazyBean lazyBean() { created.incrementAndGet(); return new LazyBean(); }
    }
    static final class LazyBean {}
}
