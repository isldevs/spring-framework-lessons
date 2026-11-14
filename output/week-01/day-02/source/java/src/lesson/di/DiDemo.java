package lesson.di;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/** Component scanning plus single-constructor dependency injection, without Boot. */
public class DiDemo {
    static final List<String> EVENTS = new ArrayList<>();

    static void event(String message) {
        EVENTS.add(message);
        System.out.println(message);
    }

    static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        event("App starts Spring with Config.class");
        try (var context = new AnnotationConfigApplicationContext()) {
            context.register(Config.class);
            // Diagnostic hook: after configuration scanning, before singleton creation.
            context.addBeanFactoryPostProcessor(beanFactory -> {
                require(beanFactory.containsBeanDefinition("repo"), "Repo definition must exist before construction");
                require(beanFactory.containsBeanDefinition("orderService"), "Service definition must exist before construction");
                event("definitions registered: repo, orderService");
            });
            context.refresh();
            event("context ready");

            require(context.containsBeanDefinition("repo"), "Repo definition must be scanned");
            require(context.containsBeanDefinition("orderService"), "Service definition must be scanned");
            require(context.getBeanDefinition("repo").getBeanClassName().equals(Repo.class.getName()),
                    "Scanned repository definition must refer to Repo");
            require(context.getBeanDefinition("orderService").getBeanClassName().equals(OrderService.class.getName()),
                    "Scanned service definition must refer to OrderService");
            require(EVENTS.indexOf("Repo created") >= 0, "Repo construction event required");
            require(EVENTS.indexOf("definitions registered: repo, orderService")
                    < EVENTS.indexOf("Repo created"), "Definitions must precede object construction");
            require(EVENTS.indexOf("Repo created") < EVENTS.indexOf("OrderService constructed with Repo"),
                    "Repository must exist before service constructor receives it");
            require(EVENTS.indexOf("OrderService constructed with Repo") < EVENTS.indexOf("context ready"),
                    "Service dependency graph must be assembled before context startup completes");
            require(OrderService.class.getDeclaredConstructors().length == 1,
                    "This example must have one constructor and needs no @Autowired annotation");
            int creationsBeforeUse = EVENTS.size();

            OrderService service = context.getBean(OrderService.class);
            Repo repository = context.getBean(Repo.class);
            boolean sameRepository = service.repo() == repository;
            require(sameRepository, "Constructor must receive the managed Repo bean");
            System.out.println("same Repo bean: " + sameRepository);
            require(service == context.getBean(OrderService.class), "Default singleton lookup must be stable");
            require(EVENTS.size() == creationsBeforeUse, "Lookup must not construct another singleton graph");
            String result = service.useRepository();
            require("ready".equals(result), "Application use must reach its injected repository");
            System.out.println("application result: " + result);
            require(context.getBeanNamesForType(Repo.class).length == 1,
                    "This demo resolves one unambiguous Repo candidate by type");
            System.out.println("scanned definitions: repo, orderService");
        }
    }
}
