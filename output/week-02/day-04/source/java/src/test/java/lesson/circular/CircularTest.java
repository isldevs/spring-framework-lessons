package lesson.circular;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.beans.factory.*;
import static org.junit.jupiter.api.Assertions.*;
class CircularTest {
 @Test void constructorCycleFailsEvenWhenCircularReferencesAllowed(){
  try(var c=new AnnotationConfigApplicationContext()){
   c.getDefaultListableBeanFactory().setAllowCircularReferences(true);
   c.register(Configs.Cycle.class);
   var ex=assertThrows(UnsatisfiedDependencyException.class,c::refresh);
   Throwable root=ex;while(root.getCause()!=null)root=root.getCause();
   assertInstanceOf(BeanCurrentlyInCreationException.class,root);assertFalse(c.isActive());
   System.out.println("constructor cycle: startup failed");
   System.out.println("outer exception: "+ex.getClass().getSimpleName());
   System.out.println("nested cause: "+root.getClass().getSimpleName());
   ex.printStackTrace(System.out);
  }
 }
 @Test void acyclicOrchestrationStartsAndExecutes(){
  try(var c=new AnnotationConfigApplicationContext()){
   c.register(Configs.Acyclic.class);c.refresh();assertTrue(c.isActive());
   var o=c.getBean(Configs.Fixed.Orchestrator.class);
   assertSame(c.getBean(Configs.Fixed.ServiceA.class),o.a());assertSame(c.getBean(Configs.Fixed.ServiceB.class),o.b());
   assertEquals(0,Configs.Fixed.ServiceA.class.getConstructors()[0].getParameterCount());
   assertEquals(0,Configs.Fixed.ServiceB.class.getConstructors()[0].getParameterCount());
   assertEquals("A then B",o.execute());
   System.out.println("acyclic context: started");System.out.println("managed references: same");System.out.println("orchestration result: "+o.execute());
  }
 }
}
