package lesson.di;

import java.util.Objects;
import org.springframework.stereotype.Service;

@Service
class OrderService {
    private final Repo repo;

    // One constructor: Spring uses it even without an @Autowired annotation.
    OrderService(Repo repo) {
        this.repo = Objects.requireNonNull(repo);
        DiDemo.event("OrderService constructed with Repo");
    }

    Repo repo() { return repo; }
    String useRepository() { return repo.read(); }
}
