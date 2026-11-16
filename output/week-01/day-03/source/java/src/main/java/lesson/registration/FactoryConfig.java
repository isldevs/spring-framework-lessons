package lesson.registration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class FactoryConfig {
    @Bean
    public Client client() {
        Trace.factoryCalls++;
        Trace.record("@Bean factory called");
        return new Client();
    }
}
