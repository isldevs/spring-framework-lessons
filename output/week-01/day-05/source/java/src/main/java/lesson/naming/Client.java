package lesson.naming;

/** A local marker object. Its name does not imply measured performance. */
public final class Client {
    private final String id;
    public Client(String id) { this.id = id; }
    public String id() { return id; }
}
