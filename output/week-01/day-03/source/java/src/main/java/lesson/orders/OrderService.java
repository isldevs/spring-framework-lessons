package lesson.orders;

import java.util.Objects;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final PaymentGateway gateway;

    // Only one constructor: Spring uses it without requiring @Autowired.
    public OrderService(PaymentGateway gateway) {
        this.gateway = Objects.requireNonNull(gateway, "gateway");
        Trace.record("OrderService constructed with PaymentGateway");
    }

    public String placeOrder(String orderId, int amountCents) {
        if (orderId == null || orderId.isBlank() || amountCents <= 0) {
            throw new IllegalArgumentException("An order ID and positive amount are required");
        }
        return gateway.charge(orderId, amountCents);
    }

    PaymentGateway gateway() { return gateway; }
}
