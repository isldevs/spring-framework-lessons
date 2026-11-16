package lesson.context;

import org.springframework.context.ApplicationEvent;

/** One explicit event so the listener ignores Spring's own lifecycle events. */
public final class DemoEvent extends ApplicationEvent {
    public DemoEvent(Object source) { super(source); }
}
