package lesson.resolution;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration(proxyBeanMethods = false)
@Import(OrderService.class)
public class SuccessConfig {
    @Bean public PaymentGateway eligibleGateway() { return new DemoPaymentGateway(); }
    @Bean(autowireCandidate = false)
    public PaymentGateway backupGateway() { return new BackupPaymentGateway(); }
    // The parameter is named gateway, but this same-named bean has the wrong type.
    @Bean("gateway") public AuditLogger unrelatedLogger() { return new AuditLogger(); }
}
