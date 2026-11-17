import org.springframework.context.annotation.*;
import org.springframework.beans.factory.UnsatisfiedDependencyException;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
public class MissingBeanDemo {
  interface Repo { String find(); }
  static class Service {
    final Repo repo;
    Service(Repo repo) { this.repo = repo; }
  }
  @Configuration(proxyBeanMethods=false)
  @Import(Service.class)
  static class Broken {}
  @Configuration(proxyBeanMethods=false)
  static class RepositoryConfig {
    @Bean Repo repo() { return () -> "ready"; }
  }
  public static void main(String[] args) {
    try (var ctx = new AnnotationConfigApplicationContext()) {
      ctx.register(Broken.class);
      try { ctx.refresh(); throw new AssertionError("Expected startup failure"); }
      catch (UnsatisfiedDependencyException expected) {
        Throwable cause = expected;
        while (cause.getCause() != null) cause = cause.getCause();
        if (!(cause instanceof NoSuchBeanDefinitionException)) throw new AssertionError(cause);
        System.out.println("startup exception: " + expected.getClass().getSimpleName());
        System.out.println("root cause: " + cause.getClass().getSimpleName());
        System.out.println("failed context active: " + ctx.isActive());
        if (ctx.isActive()) throw new AssertionError("Failed context active");
      }
    }
    try (var ctx = new AnnotationConfigApplicationContext()) {
      ctx.register(Broken.class, RepositoryConfig.class);
      ctx.refresh();
      Service service = ctx.getBean(Service.class);
      if (!ctx.isActive() || service.repo != ctx.getBean(Repo.class)) throw new AssertionError("Wiring failed");
      if (!service.repo.find().equals("ready")) throw new AssertionError("Business use failed");
      System.out.println("fixed context active: " + ctx.isActive());
      System.out.println("same repository: true");
      System.out.println("business result: " + service.repo.find());
    }
  }
}
