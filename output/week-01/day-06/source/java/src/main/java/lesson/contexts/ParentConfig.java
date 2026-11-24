package lesson.contexts;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class ParentConfig {
    @Bean("shared")
    Item shared() { return new Item("shared"); }
}
