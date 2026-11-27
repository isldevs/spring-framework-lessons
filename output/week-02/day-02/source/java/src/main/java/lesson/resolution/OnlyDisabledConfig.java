package lesson.resolution;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration(proxyBeanMethods = false)
@Import(OrderService.class)
public class OnlyDisabledConfig {
    @Bean(autowireCandidate = false)
    public PaymentGateway backupGateway() { return new BackupPaymentGateway(); }
    @Bean("gateway") public AuditLogger unrelatedLogger() { return new AuditLogger(); }
}
