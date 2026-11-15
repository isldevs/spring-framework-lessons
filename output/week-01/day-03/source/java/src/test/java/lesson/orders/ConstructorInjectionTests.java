package lesson.orders;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.springframework.boot.SpringBootVersion;
import org.springframework.context.ConfigurableApplicationContext;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(OrderAnnotation.class)
class ConstructorInjectionTests {
    @Test @Order(1)
    void bootInjectsTheManagedGatewayBeforeOrderUse() {
        System.out.println("BOOT INTEGRATION TEST");
        Trace.clear();
        Trace.record("App starts Spring Boot");
        try (ConfigurableApplicationContext context = CheckoutApplication.start()) {
            Trace.record("Boot context ready");
            OrderService service = context.getBean(OrderService.class);
            PaymentGateway gateway = context.getBean(PaymentGateway.class);
            assertEquals("3.5.6", SpringBootVersion.getVersion());
            assertEquals(1, context.getBeansOfType(PaymentGateway.class).size());
            assertSame(gateway, service.gateway());
            assertInstanceOf(DemoGateway.class, gateway);
            List<String> events = Trace.snapshot();
            int gatewayAt = events.indexOf("DemoGateway created");
            int serviceAt = events.indexOf("OrderService constructed with PaymentGateway");
            int readyAt = events.indexOf("Boot context ready");
            assertTrue(gatewayAt >= 0 && gatewayAt < serviceAt && serviceAt < readyAt);
            assertEquals(0, ((DemoGateway) gateway).calls());
            System.out.println("same gateway bean: true");
            String receipt = service.placeOrder("order-1042", 1999);
            assertEquals("APPROVED order-1042 USD 19.99", receipt);
            assertEquals(1, ((DemoGateway) gateway).calls());
            assertSame(service, context.getBean(OrderService.class));
            System.out.println("receipt: " + receipt);
            System.out.println("Spring Boot integration test: passed");
        }
    }

    @Test @Order(2)
    void aRecordingFakeTestsOrderForwardingWithoutSpring() {
        System.out.println("PURE JAVA SERVICE TEST");
        RecordingGateway fake = new RecordingGateway();
        OrderService service = new OrderService(fake);
        String result = service.placeOrder("order-test", 2500);
        assertEquals("order-test", fake.orderId);
        assertEquals(2500, fake.amountCents);
        assertEquals(1, fake.calls);
        assertEquals("FAKE_APPROVED", result);
        System.out.println("fake gateway test: passed");
    }

    private static final class RecordingGateway implements PaymentGateway {
        private String orderId;
        private int amountCents;
        private int calls;
        @Override public String charge(String orderId, int amountCents) {
            this.orderId = orderId; this.amountCents = amountCents; calls++;
            return "FAKE_APPROVED";
        }
    }
}
