package lesson.contexts;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class BConfig {
    @Bean("beta")
    Item beta() { return new Item("beta"); }
}
