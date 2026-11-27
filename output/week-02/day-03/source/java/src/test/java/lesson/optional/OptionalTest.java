package lesson.optional;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.beans.factory.*;
import static org.junit.jupiter.api.Assertions.*;
class OptionalTest {
 AnnotationConfigApplicationContext context(Class<?> config){ var c=new AnnotationConfigApplicationContext();c.register(config);return c; }
 Throwable root(Throwable t){while(t.getCause()!=null)t=t.getCause();return t;}
 @Test void requiredAbsentFails(){try(var c=context(Configs.RequiredAbsent.class)){
 var ex=assertThrows(UnsatisfiedDependencyException.class,c::refresh);
 assertInstanceOf(NoSuchBeanDefinitionException.class,root(ex));assertFalse(c.isActive());
 System.out.println("required absent: startup failed");System.out.println("required root: "+root(ex).getClass().getSimpleName());}}
 @Test void optionalAbsentStartsEmpty(){try(var c=context(Configs.OptionalAbsent.class)){
 c.refresh();assertTrue(c.isActive());var s=c.getBean(Configs.OptionalService.class);assertTrue(s.audit().isEmpty());assertDoesNotThrow(s::notifyIfPresent);
 System.out.println("optional absent: started, empty=true");}}
 @Test void optionalPresentStartsWithSameReference(){try(var c=context(Configs.OptionalPresent.class)){
 c.refresh();assertTrue(c.isActive());var a=c.getBean(Configs.AuditPublisher.class);var s=c.getBean(Configs.OptionalService.class);
 assertTrue(s.audit().isPresent());assertSame(a,s.audit().orElseThrow());assertDoesNotThrow(s::notifyIfPresent);
 System.out.println("optional present: started, same=true");}}
 @Test void optionalDoesNotHideAmbiguity(){try(var c=context(Configs.Ambiguous.class)){
 var ex=assertThrows(UnsatisfiedDependencyException.class,c::refresh);assertInstanceOf(NoUniqueBeanDefinitionException.class,root(ex));assertFalse(c.isActive());
 System.out.println("optional ambiguity: startup failed");System.out.println("ambiguity root: "+root(ex).getClass().getSimpleName());}}
}
