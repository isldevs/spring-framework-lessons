package lesson.constructor;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration(proxyBeanMethods = false)
@Import({OrderService.class, DemoPaymentGateway.class})
public class Config {
}
