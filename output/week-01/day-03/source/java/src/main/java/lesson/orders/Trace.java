package lesson.orders;

import java.util.ArrayList;
import java.util.List;

/** Local diagnostic, not a bean and not needed by constructor injection. */
final class Trace {
    private static final List<String> EVENTS = new ArrayList<>();
    static void clear() { EVENTS.clear(); }
    static void record(String event) { EVENTS.add(event); System.out.println(event); }
    static List<String> snapshot() { return List.copyOf(EVENTS); }
    private Trace() {}
}
