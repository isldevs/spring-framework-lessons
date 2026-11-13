import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Minimal manual-vs-Spring object creation and wiring demonstration. */
public class IoCDemo {
    static final class Repo {}

    static final class Service {
        private final Repo repo;
        Service(Repo repo) { this.repo = repo; }
        Repo repo() { return repo; }
    }

    @Configuration
    static class Config {
        @Bean
        Repo repo() { return new Repo(); }

        @Bean
        Service service(Repo repo) { return new Service(repo); }
    }

    // The alias ctx is owned and closed by the try-with-resources variable context.
    @SuppressWarnings("resource")
    public static void main(String[] args) {
        // Manual construction: application code chooses and wires both objects.
        Repo manualRepo = new Repo();
        Service manualService = new Service(manualRepo);
        check("manual wiring", manualService.repo() == manualRepo);

        // Spring reads Config, creates the registered beans, and resolves Repo.
        try (var context = new AnnotationConfigApplicationContext(Config.class)) {
            ApplicationContext ctx = context;
            // The application requests its already-wired dependency.
            Service service = ctx.getBean(Service.class);
            Repo repo = ctx.getBean(Repo.class);
            check("spring wiring", service.repo() == repo);
            check("same singleton", service == ctx.getBean(Service.class));

            // A Java object created independently is not automatically a bean.
            Repo unmanaged = new Repo();
            boolean unmanagedSame = unmanaged == repo;
            if (unmanagedSame) throw new AssertionError("Independent new unexpectedly identical");
            System.out.println("unmanaged same as bean: " + unmanagedSame);
        }
    }

    private static void check(String label, boolean result) {
        if (!result) throw new AssertionError(label);
        System.out.println(label + ": " + result);
    }
}
