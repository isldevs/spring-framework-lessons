package lesson.orders;

/** Port for submitting a payment. The included implementation is a local demo. */
public interface PaymentGateway {
    String charge(String orderId, int amountCents);
}
