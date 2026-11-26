package lesson.constructor;

import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final PaymentGateway gateway;

    // The single constructor is intentionally not annotated with @Autowired.
    public OrderService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public String placeOrder(int cents) {
        return gateway.charge(cents);
    }

    public PaymentGateway gateway() {
        return gateway;
    }
}
