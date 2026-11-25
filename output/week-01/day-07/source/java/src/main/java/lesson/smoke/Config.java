package lesson.smoke;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class Config {
    @Bean
    Repo repo() {
        return new Repo();
    }

    @Bean
    OrderService service(Repo repo) {
        return new OrderService(repo);
    }
}
