package lesson.registration;

import lesson.scan.Worker;
import lesson.outside.Outside;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public final class RegistrationDemo {
    public static void main(String[] args) {
        Trace.clear();
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.refresh();
            Trace.record("plain class missing: " + missing(ctx, Client.class));
            require(Trace.clients == 0, "Unregistered Client was instantiated");
        }
        Trace.clear();
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(FactoryConfig.class);
            ctx.addBeanFactoryPostProcessor(factory -> {
                require(factory.containsBeanDefinition("client"), "No factory definition");
                require(!factory.containsSingleton("client"), "Client created before observation");
                Trace.record("@Bean definition: client");
            });
            ctx.refresh();
            Client client = ctx.getBean(Client.class);
            require(client.name().equals("explicit"), "Wrong factory bean");
            require(Trace.clients == 1 && Trace.factoryCalls == 1, "Unexpected factory count");
            Trace.record("@Bean retrieved: " + (client == ctx.getBean("client")));
        }
        Trace.clear();
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(ScanConfig.class);
            ctx.addBeanFactoryPostProcessor(factory -> {
                require(factory.containsBeanDefinition("worker"), "No scanned definition");
                require(!factory.containsSingleton("worker"), "Worker created before observation");
                Trace.record("scan definition: worker");
            });
            ctx.refresh();
            Worker worker = ctx.getBean(Worker.class);
            require(worker.name().equals("scanned"), "Wrong scanned bean");
            require(Trace.workers == 1, "Unexpected Worker count");
            Trace.record("scan retrieved: " + (worker == ctx.getBean("worker")));
            Trace.record("outside scan missing: " + missing(ctx, Outside.class));
            require(Trace.outsiders == 0, "Outside-package component was instantiated");
        }
    }
    private static boolean missing(AnnotationConfigApplicationContext ctx, Class<?> type) {
        try { ctx.getBean(type); }
        catch (NoSuchBeanDefinitionException expected) { return true; }
        throw new IllegalStateException("Expected no bean for " + type.getName());
    }
    private static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
}
