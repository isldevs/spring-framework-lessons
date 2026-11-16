package lesson.context;

import java.util.Objects;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.context.ApplicationListener;

/** A managed object with a dependency, event listener and cleanup callback. */
public final class Service implements ApplicationListener<DemoEvent>, DisposableBean {
    private final Repo repo;
    public Service(Repo repo) {
        this.repo = Objects.requireNonNull(repo, "repo");
        Trace.services++; Trace.record("service created with repo");
    }
    public Repo repo() { return repo; }
    public String run() { return repo.message(); }
    @Override public void onApplicationEvent(DemoEvent event) { Trace.handled++; }
    @Override public void destroy() { Trace.cleanup++; Trace.record("service cleanup"); }
}
