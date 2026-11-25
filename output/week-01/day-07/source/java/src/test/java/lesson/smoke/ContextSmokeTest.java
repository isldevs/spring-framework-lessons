package lesson.smoke;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.core.SpringVersion;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringJUnitConfig(Config.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class ContextSmokeTest {
    @Autowired
    ApplicationContext ctx;

    @Test
    void contextLoadsAndWires() {
        assertEquals("6.2.11", SpringVersion.getVersion());
        OrderService service = ctx.getBean(OrderService.class);
        Repo repo = ctx.getBean(Repo.class);
        assertNotNull(service);
        assertNotNull(repo);
        assertSame(repo, service.repository());

        // These proof lines are emitted only after the real assertions pass.
        System.out.println("bean found: " + (service != null));
        System.out.println("wiring same: " + (repo == service.repository()));
    }
}
