package lesson.naming;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class BetaConfig {
    @Bean("beta") public Client backup() { return new Client("beta"); }
}
