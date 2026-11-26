package lesson.constructor;

import org.springframework.stereotype.Component;

/** In-memory demonstration only: no network or real payment is performed. */
@Component
public class DemoPaymentGateway implements PaymentGateway {
    @Override
    public String charge(int cents) {
        return "demo-paid:" + cents;
    }
}
