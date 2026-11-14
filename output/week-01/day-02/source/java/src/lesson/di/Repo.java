package lesson.di;

import org.springframework.stereotype.Repository;

@Repository
class Repo {
    Repo() { DiDemo.event("Repo created"); }
    String read() { return "ready"; }
}
