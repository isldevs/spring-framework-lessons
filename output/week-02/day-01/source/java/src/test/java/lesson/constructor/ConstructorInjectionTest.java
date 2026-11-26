package lesson.constructor;

import java.lang.reflect.Constructor;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.core.SpringVersion;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import static org.junit.jupiter.api.Assertions.*;

@SpringJUnitConfig(Config.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class ConstructorInjectionTest {
    @Autowired
    ApplicationContext ctx;

    @Test
    void springUsesTheOnlyConstructorWithoutAutowired() {
        assertEquals("6.2.11", SpringVersion.getVersion());
        Constructor<?>[] constructors = OrderService.class.getDeclaredConstructors();
        assertEquals(1, constructors.length);
        assertFalse(constructors[0].isAnnotationPresent(Autowired.class));
        assertArrayEquals(new Class<?>[] { PaymentGateway.class }, constructors[0].getParameterTypes());
        assertEquals(1, ctx.getBeansOfType(PaymentGateway.class).size());

        OrderService service = ctx.getBean(OrderService.class);
        PaymentGateway gateway = ctx.getBean(PaymentGateway.class);
        assertNotNull(service);
        assertSame(gateway, service.gateway());
        String result = service.placeOrder(2500);
        assertEquals("demo-paid:2500", result);

        // Literal proof is printed only after the real assertions pass.
        System.out.println("constructors: " + constructors.length);
        System.out.println("autowired: " + constructors[0].isAnnotationPresent(Autowired.class));
        System.out.println("gateway same: " + (gateway == service.gateway()));
        System.out.println("order result: " + result);
    }

    @Test
    void newUsesOnlyTheCallerSuppliedArgument() {
        PaymentGateway callerGateway = new DemoPaymentGateway();
        OrderService manual = new OrderService(callerGateway);
        OrderService managed = ctx.getBean(OrderService.class);
        PaymentGateway contextGateway = ctx.getBean(PaymentGateway.class);

        assertSame(callerGateway, manual.gateway());
        assertNotSame(contextGateway, manual.gateway());
        assertNotSame(managed, manual);
        assertEquals("demo-paid:2500", manual.placeOrder(2500));
        System.out.println("manual uses caller: " + (callerGateway == manual.gateway()));
    }
}
