package lesson.context;

import java.util.ArrayList;
import java.util.List;

/** Single-threaded observations for this tiny reproducible demonstration. */
public final class Trace {
    private static final List<String> events = new ArrayList<>();
    static int repos;
    static int services;
    static int handled;
    static int cleanup;
    private Trace() {}
    public static void clear() {
        events.clear(); repos = 0; services = 0; handled = 0; cleanup = 0;
    }
    public static void record(String event) { events.add(event); System.out.println(event); }
    public static List<String> snapshot() { return List.copyOf(events); }
}
