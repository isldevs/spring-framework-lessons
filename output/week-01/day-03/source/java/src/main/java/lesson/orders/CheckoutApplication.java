package lesson.orders;

import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication(proxyBeanMethods = false)
public class CheckoutApplication {
    public static ConfigurableApplicationContext start() {
        SpringApplication application = new SpringApplication(CheckoutApplication.class);
        application.setWebApplicationType(WebApplicationType.NONE);
        application.setBannerMode(Banner.Mode.OFF);
        application.setLogStartupInfo(false);
        application.setRegisterShutdownHook(false);
        return application.run("--logging.level.root=OFF");
    }
    public static void main(String[] args) {
        try (ConfigurableApplicationContext context = start()) {
            OrderService orders = context.getBean(OrderService.class);
            System.out.println("receipt: " + orders.placeOrder("order-1042", 1999));
        }
    }
}
