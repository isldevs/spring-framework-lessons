package lesson.optional;
import java.util.Optional;
import org.springframework.context.annotation.*;
public class Configs {
 public interface AuditPublisher { void publish(); }
 public static class RequiredService { public RequiredService(AuditPublisher audit) {} }
 public static class OptionalService {
  private final Optional<AuditPublisher> audit;
  public OptionalService(Optional<AuditPublisher> audit) { this.audit=audit; }
  public Optional<AuditPublisher> audit(){ return audit; }
  public void notifyIfPresent(){ audit.ifPresent(AuditPublisher::publish); }
 }
 @Configuration @Import(RequiredService.class) public static class RequiredAbsent {}
 @Configuration @Import(OptionalService.class) public static class OptionalAbsent {}
 @Configuration @Import(OptionalService.class) public static class OptionalPresent {
  @Bean AuditPublisher auditPublisher(){return () -> {};}
 }
 @Configuration @Import(OptionalService.class) public static class Ambiguous {
  @Bean AuditPublisher first(){return () -> {};}
  @Bean AuditPublisher second(){return () -> {};}
 }
}
