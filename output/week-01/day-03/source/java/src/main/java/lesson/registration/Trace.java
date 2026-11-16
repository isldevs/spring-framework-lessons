package lesson.registration;

import java.util.ArrayList;
import java.util.List;

/** Single-threaded observations for this minimal demonstration and its tests. */
public final class Trace {
    private static final List<String> events = new ArrayList<>();
    public static int clients;
    public static int workers;
    public static int outsiders;
    public static int factoryCalls;
    private Trace() {}
    public static void clear() {
        events.clear(); clients = 0; workers = 0; outsiders = 0; factoryCalls = 0;
    }
    public static void record(String event) { events.add(event); System.out.println(event); }
    public static List<String> snapshot() { return List.copyOf(events); }
}
