package lesson.contexts;

import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public final class ContextsDemo {
    public static void main(String[] args) {
        try (var a = new AnnotationConfigApplicationContext(AConfig.class);
             var b = new AnnotationConfigApplicationContext(BConfig.class)) {
            System.out.println("A alpha: " + a.getBean("alpha", Item.class).id());
            System.out.println("B beta: " + b.getBean("beta", Item.class).id());
            missing(a, "beta", "A beta");
            missing(b, "alpha", "B alpha");
        }
        // These are fresh contexts, not a reconfiguration of the running A/B pair.
        try (var parent = new AnnotationConfigApplicationContext(ParentConfig.class)) {
            try (var child = new AnnotationConfigApplicationContext()) {
                child.setParent(parent);
                child.register(ChildConfig.class);
                child.refresh();
                Item inherited = child.getBean("shared", Item.class);
                require(inherited == parent.getBean("shared", Item.class), "Parent reference differs");
                require(!child.containsLocalBean("shared"), "Parent bean was copied locally");
                System.out.println("child shared: " + inherited.id());
                System.out.println("child shared same: " +
                        (inherited == parent.getBean("shared", Item.class)));
                System.out.println("child owns shared: " + child.containsLocalBean("shared"));
                System.out.println("child local: " + child.getBean("local", Item.class).id());
                missing(parent, "local", "parent local");
            }
            require(parent.isActive(), "Closing child closed parent");
            System.out.println("parent active after child close: " + parent.isActive());
        }
    }

    private static void missing(AnnotationConfigApplicationContext context, String name, String label) {
        try {
            context.getBean(name);
            throw new AssertionError("Expected missing bean " + name);
        } catch (NoSuchBeanDefinitionException expected) {
            require(name.equals(expected.getBeanName()), "Unexpected missing name");
            System.out.println(label + ": missing");
            System.out.println(label + " exception: " + expected.getClass().getSimpleName());
        }
    }

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
