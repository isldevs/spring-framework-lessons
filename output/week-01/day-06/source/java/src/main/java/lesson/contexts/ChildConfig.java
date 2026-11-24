package lesson.contexts;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class ChildConfig {
    @Bean("local")
    Item local() { return new Item("local"); }
}
