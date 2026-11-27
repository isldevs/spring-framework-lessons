package lesson.resolution;

public final class BackupPaymentGateway implements PaymentGateway {
    @Override public String id() { return "backup"; }
}
