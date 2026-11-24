package lesson.contexts;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class AConfig {
    @Bean("alpha")
    Item alpha() { return new Item("alpha"); }
}
