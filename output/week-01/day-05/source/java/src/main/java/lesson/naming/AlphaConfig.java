package lesson.naming;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class AlphaConfig {
    @Bean("alpha") public Client client() { return new Client("alpha"); }
}
