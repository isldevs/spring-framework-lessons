package lesson.scan;

import lesson.registration.Trace;
import org.springframework.stereotype.Component;

@Component
public final class Worker {
    public Worker() { Trace.workers++; Trace.record("Worker created"); }
    public String name() { return "scanned"; }
}
