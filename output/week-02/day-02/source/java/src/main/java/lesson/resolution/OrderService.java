package lesson.resolution;

import org.springframework.stereotype.Service;

@Service
public final class OrderService {
    private final PaymentGateway gateway;

    public OrderService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public PaymentGateway gateway() { return gateway; }
}
