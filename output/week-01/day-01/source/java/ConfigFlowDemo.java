import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Trace the configuration-to-object flow used by the closing diagram. */
public class ConfigFlowDemo {
    private static final List<String> EVENTS = new ArrayList<>();
    private static int factoryCalls;

    static final class Repo {}

    static final class Service {
        private final Repo repo;
        Service(Repo repo) { this.repo = repo; }
        Repo repo() { return repo; }
    }

    @Configuration
    static class Config {
        Config() { event("Spring instantiates Config"); }

        @Bean
        Repo repo() {
            factoryCalls++;
            event("Spring calls Config.repo(): create Repo");
            return new Repo();
        }

        @Bean
        Service service(Repo repo) {
            factoryCalls++;
            event("Spring calls Config.service(repo): wire Repo into Service");
            return new Service(repo);
        }
    }

    public static void main(String[] args) {
        event("App starts Spring with Config.class");
        try (var context = new AnnotationConfigApplicationContext(Config.class)) {
            event("Spring context is ready");
            require(factoryCalls == 2, "Both default singleton factories must run at startup");
            require(EVENTS.indexOf("Spring calls Config.repo(): create Repo")
                    < EVENTS.indexOf("Spring calls Config.service(repo): wire Repo into Service"),
                    "Repo must exist before Service receives it");
            require(EVENTS.indexOf("Spring calls Config.service(repo): wire Repo into Service")
                    < EVENTS.indexOf("Spring context is ready"),
                    "Service must be wired before startup completes");

            int callsBeforeLookup = factoryCalls;
            event("App calls getBean(Service.class)");
            Service first = context.getBean(Service.class);
            boolean repositoryMatches = first.repo() == context.getBean(Repo.class);
            require(repositoryMatches, "Service must hold the container's Repo bean");
            System.out.println("same Repo bean: " + repositoryMatches);

            event("App calls getBean(Service.class) again");
            Service second = context.getBean(Service.class);
            boolean sameService = first == second;
            require(sameService, "Default singleton lookup must return the same Service");
            require(factoryCalls == callsBeforeLookup, "Lookups must not call factories again");
            System.out.println("same Service bean: " + sameService);
            System.out.println("factory calls after lookups: " + factoryCalls + " (unchanged)");
        }
    }

    private static void event(String message) {
        EVENTS.add(message);
        System.out.println(message);
    }

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
