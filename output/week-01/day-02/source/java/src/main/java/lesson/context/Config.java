package lesson.context;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class Config {
    @Bean public Repo repo() { return new Repo(); }
    @Bean public Service service(Repo repo) { return new Service(repo); }
}
