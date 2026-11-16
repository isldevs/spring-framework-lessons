package lesson.registration;

/** Plain Java class: registration comes from FactoryConfig's @Bean method. */
public final class Client {
    public Client() { Trace.clients++; Trace.record("Client created"); }
    public String name() { return "explicit"; }
}
