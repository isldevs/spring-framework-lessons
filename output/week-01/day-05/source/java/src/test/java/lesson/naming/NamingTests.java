package lesson.naming;

import java.util.Set;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.BeanNotOfRequiredTypeException;
import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.core.SpringVersion;
import static org.junit.jupiter.api.Assertions.*;

class NamingTests {
    @Test
    void explicitNameReplacesDefaultMethodNameAndAllSingleLookupsAgree() {
        try (var ctx = new AnnotationConfigApplicationContext(AlphaConfig.class)) {
            assertEquals("6.2.11", SpringVersion.getVersion());
            assertTrue(ctx.containsBeanDefinition("alpha"));
            assertFalse(ctx.containsBean("client"));
            var definition = ctx.getBeanFactory().getBeanDefinition("alpha");
            assertEquals("client", definition.getFactoryMethodName());
            assertTrue(definition.isSingleton());
            Client alpha = ctx.getBean("alpha", Client.class);
            assertEquals("alpha", alpha.id());
            assertSame(alpha, ctx.getBean("alpha"));
            assertSame(alpha, ctx.getBean(Client.class));
            assertEquals(1, ctx.getBeansOfType(Client.class).size());
            System.out.println("single named/type identity: passed");
        }
    }

    @Test
    void distinctNamesDoNotChooseBetweenTwoUnprioritizedTypeCandidates() {
        try (var ctx = new AnnotationConfigApplicationContext(AlphaConfig.class, BetaConfig.class)) {
            assertEquals(Set.of("alpha", "beta"), ctx.getBeansOfType(Client.class).keySet());
            assertFalse(ctx.getBeanFactory().getBeanDefinition("alpha").isPrimary());
            assertFalse(ctx.getBeanFactory().getBeanDefinition("beta").isPrimary());
            Client alpha = ctx.getBean("alpha", Client.class);
            Client beta = ctx.getBean("beta", Client.class);
            assertNotSame(alpha, beta);
            assertEquals("alpha", alpha.id());
            assertEquals("beta", beta.id());
            NoUniqueBeanDefinitionException failure = assertThrows(NoUniqueBeanDefinitionException.class,
                    () -> ctx.getBean(Client.class));
            assertEquals(2, failure.getNumberOfBeansFound());
            assertEquals(Set.of("alpha", "beta"), Set.copyOf(failure.getBeanNamesFound()));
            System.out.println("two named beans/type ambiguity: passed");
        }
    }

    @Test
    void namedLookupWithTypeChecksTheSelectedBeansType() {
        try (var ctx = new AnnotationConfigApplicationContext(AlphaConfig.class, BetaConfig.class)) {
            BeanNotOfRequiredTypeException failure = assertThrows(BeanNotOfRequiredTypeException.class,
                    () -> ctx.getBean("alpha", String.class));
            assertEquals("alpha", failure.getBeanName());
            assertEquals(String.class, failure.getRequiredType());
            assertEquals(Client.class, failure.getActualType());
            assertSame(ctx.getBean("alpha"), ctx.getBean("alpha", Client.class));
            System.out.println("named type check: passed");
        }
    }

    @Test
    void qualifierSelectsInjectionWithoutChangingTheTypeOnlyLookup() {
        try (var ctx = new AnnotationConfigApplicationContext(AlphaConfig.class, BetaConfig.class, ConsumerConfig.class)) {
            QualifiedConsumer consumer = ctx.getBean(QualifiedConsumer.class);
            assertSame(ctx.getBean("beta"), consumer.client);
            assertEquals("beta", consumer.client.id());
            assertThrows(NoUniqueBeanDefinitionException.class, () -> ctx.getBean(Client.class));
            assertEquals(Set.of("alpha", "beta"), ctx.getBeansOfType(Client.class).keySet());
            System.out.println("qualifier injection remains distinct: passed");
        }
    }

    @Configuration(proxyBeanMethods = false)
    @Import(QualifiedConsumer.class)
    static class ConsumerConfig {}

    static class QualifiedConsumer {
        final Client client;
        QualifiedConsumer(@Qualifier("beta") Client client) { this.client = client; }
    }
}
