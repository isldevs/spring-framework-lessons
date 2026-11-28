package lesson.circular;
import org.springframework.context.annotation.*;
public class Configs {
 public static class Broken {
  public static class ServiceA { public ServiceA(ServiceB b) {} }
  public static class ServiceB { public ServiceB(ServiceA a) {} }
 }
 @Configuration @Import({Broken.ServiceA.class,Broken.ServiceB.class}) public static class Cycle {}
 public static class Fixed {
  public static class ServiceA { public String prepare(){return "A";} }
  public static class ServiceB { public String finish(){return "B";} }
  public static class Orchestrator {
   private final ServiceA a;private final ServiceB b;
   public Orchestrator(ServiceA a,ServiceB b){this.a=a;this.b=b;}
   public ServiceA a(){return a;} public ServiceB b(){return b;}
   public String execute(){return a.prepare()+" then "+b.finish();}
  }
 }
 @Configuration @Import({Fixed.ServiceA.class,Fixed.ServiceB.class,Fixed.Orchestrator.class}) public static class Acyclic {}
}
