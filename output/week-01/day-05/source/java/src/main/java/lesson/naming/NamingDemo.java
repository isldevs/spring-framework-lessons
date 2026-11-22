package lesson.naming;

import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public final class NamingDemo {
    public static void main(String[] args) {
        try (var ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(AlphaConfig.class);
            ctx.refresh();
            Client named = (Client) ctx.getBean("alpha");
            Client checked = ctx.getBean("alpha", Client.class);
            Client typed = ctx.getBean(Client.class);
            require(named == checked && named == typed, "Single lookups differ");
            require(!ctx.containsBean("client"), "Factory method became an extra name");
            System.out.println("named alpha: " + named.id());
            System.out.println("typed name alpha: " + checked.id());
            System.out.println("single type same: " + (typed == named));
        }
        try (var ctx = new AnnotationConfigApplicationContext()) {
            ctx.register(AlphaConfig.class, BetaConfig.class);
            ctx.refresh();
            Client alpha = ctx.getBean("alpha", Client.class);
            Client beta = ctx.getBean("beta", Client.class);
            require(alpha != beta, "Expected distinct beans");
            require(ctx.getBeansOfType(Client.class).size() == 2, "Expected two clients");
            System.out.println("named beta: " + beta.id());
            try {
                ctx.getBean(Client.class);
                throw new AssertionError("Expected ambiguous type lookup");
            } catch (NoUniqueBeanDefinitionException expected) {
                require(expected.getNumberOfBeansFound() == 2, "Wrong candidate count");
                System.out.println("type lookup: " + expected.getClass().getSimpleName());
                System.out.println("type candidates: " + expected.getNumberOfBeansFound());
                System.out.println("type message: " + expected.getMessage());
            }
        }
    }
    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
