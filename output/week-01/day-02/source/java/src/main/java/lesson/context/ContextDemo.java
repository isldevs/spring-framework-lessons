package lesson.context;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public final class ContextDemo {
    public static void main(String[] args) {
        Trace.clear();
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            Trace.record("context created");
            ctx.register(Config.class);
            Trace.record("configuration registered");
            // This runs after @Configuration processing registers @Bean definitions,
            // and before these ordinary application singletons are instantiated.
            ctx.addBeanFactoryPostProcessor(factory -> {
                if (!factory.containsBeanDefinition("repo") || !factory.containsBeanDefinition("service")) {
                    throw new IllegalStateException("Missing application definitions");
                }
                Trace.record("bean definitions: repo, service");
                Trace.record("instances at definition stage: " + (Trace.repos + Trace.services));
            });
            ctx.refresh();
            Trace.record("context refreshed");
            Service first = ctx.getBean(Service.class);
            Service again = ctx.getBean(Service.class);
            Trace.record("same service: " + (first == again));
            Trace.record("service result: " + first.run());
            ctx.publishEvent(new DemoEvent(ctx));
            Trace.record("events handled: " + Trace.handled);
        }
        Trace.record("cleanup called: " + (Trace.cleanup == 1));
    }
}
