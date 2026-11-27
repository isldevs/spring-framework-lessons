package lesson.resolution;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration(proxyBeanMethods = false)
@Import(OrderService.class)
public class MissingConfig {
    @Bean("gateway") public AuditLogger unrelatedLogger() { return new AuditLogger(); }
}
