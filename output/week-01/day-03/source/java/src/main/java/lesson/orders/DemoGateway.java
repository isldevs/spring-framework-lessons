package lesson.orders;

import java.util.Locale;
import org.springframework.stereotype.Component;

/** Simulates approval in memory. It does not contact a processor or move money. */
@Component
public class DemoGateway implements PaymentGateway {
    private int calls;
    public DemoGateway() {
        Trace.record("DemoGateway created");
    }
    @Override
    public String charge(String orderId, int amountCents) {
        calls++;
        return String.format(Locale.ROOT, "APPROVED %s USD %d.%02d", orderId,
                amountCents / 100, amountCents % 100);
    }
    int calls() { return calls; }
}
