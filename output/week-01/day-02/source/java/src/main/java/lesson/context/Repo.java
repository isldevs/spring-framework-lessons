package lesson.context;

public final class Repo {
    public Repo() { Trace.repos++; Trace.record("repo created"); }
    public String message() { return "hello from repo"; }
}
