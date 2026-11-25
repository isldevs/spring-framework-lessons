package lesson.smoke;

/** Exposes the collaborator only to make this small wiring example explicit. */
public final class OrderService {
    private final Repo repository;

    public OrderService(Repo repository) {
        this.repository = repository;
    }

    public Repo repository() {
        return repository;
    }
}
