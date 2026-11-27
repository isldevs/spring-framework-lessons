package lesson.resolution;

import java.util.Set;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.beans.factory.UnsatisfiedDependencyException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.SpringVersion;
import static org.junit.jupiter.api.Assertions.*;

class DependencyResolutionTest {
    @Test
    void compatibleTypesAreFilteredBeforeTheExpectedGatewayIsInjected() throws Exception {
        TracingBeanFactory factory = new TracingBeanFactory();
        try (var context = new AnnotationConfigApplicationContext(factory)) {
            context.register(SuccessConfig.class);
            context.refresh();
            assertEquals("6.2.11", SpringVersion.getVersion());
            assertEquals("gateway", OrderService.class.getDeclaredConstructors()[0]
                    .getParameters()[0].getName());
            OrderService service = context.getBean(OrderService.class);
            PaymentGateway expected = context.getBean("eligibleGateway", PaymentGateway.class);
            assertSame(expected, service.gateway());
            assertEquals("eligible", service.gateway().id());
            assertInstanceOf(AuditLogger.class, context.getBean("gateway"));
            assertEquals(Set.of("eligibleGateway", "backupGateway"),
                    Set.copyOf(factory.compatibleNames));
            assertEquals(Set.of("eligibleGateway"), Set.copyOf(factory.eligibleNames));
            assertFalse(factory.compatibleNames.contains("gateway"));
            assertEquals(Boolean.FALSE, factory.candidateDecisions.get("backupGateway"));
            assertEquals(Boolean.TRUE, factory.candidateDecisions.get("eligibleGateway"));
            assertNotSame(expected, context.getBean("backupGateway", PaymentGateway.class));
            assertTrue(context.containsBean("backupGateway"));
            factory.events.forEach(event -> System.out.println("TRACE " + event));
            System.out.println("compatible candidates: " + factory.compatibleNames.size());
            System.out.println("eligible candidates: " + factory.eligibleNames.size());
            System.out.println("unrelated ignored: " + !factory.compatibleNames.contains("gateway"));
            System.out.println("gateway same: " + (expected == service.gateway()));
        }
    }

    @Test
    void missingRequiredTypeFailsContextStartup() {
        TracingBeanFactory factory = new TracingBeanFactory();
        try (var context = new AnnotationConfigApplicationContext(factory)) {
            context.register(MissingConfig.class);
            UnsatisfiedDependencyException failure = assertThrows(UnsatisfiedDependencyException.class,
                    context::refresh);
            Throwable root = deepest(failure);
            assertInstanceOf(NoSuchBeanDefinitionException.class, root);
            assertTrue(factory.compatibleNames.isEmpty());
            assertTrue(factory.eligibleNames.isEmpty());
            assertFalse(context.isActive());
            System.out.println("missing candidate: true");
            System.out.println("missing exception: " + root.getClass().getSimpleName());
            System.out.println("missing startup exception: " + failure.getClass().getSimpleName());
        }
    }

    @Test
    void matchingButDisabledBeanStillLeavesNoEligibleCandidate() {
        TracingBeanFactory factory = new TracingBeanFactory();
        try (var context = new AnnotationConfigApplicationContext(factory)) {
            context.register(OnlyDisabledConfig.class);
            UnsatisfiedDependencyException failure = assertThrows(UnsatisfiedDependencyException.class,
                    context::refresh);
            assertInstanceOf(NoSuchBeanDefinitionException.class, deepest(failure));
            assertEquals(Set.of("backupGateway"), Set.copyOf(factory.compatibleNames));
            assertTrue(factory.eligibleNames.isEmpty());
            assertEquals(Boolean.FALSE, factory.candidateDecisions.get("backupGateway"));
            assertFalse(context.isActive());
            System.out.println("disabled candidate missing: true");
            System.out.println("disabled compatible candidates: " + factory.compatibleNames.size());
            System.out.println("disabled eligible candidates: " + factory.eligibleNames.size());
        }
    }

    private static Throwable deepest(Throwable failure) {
        while (failure.getCause() != null) failure = failure.getCause();
        return failure;
    }
}
