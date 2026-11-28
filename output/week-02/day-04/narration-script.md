# Circular dependencies — narration

Approved topic Circular dependencies; publication2026-11-26 proposed19:00Asia/Phnom_Penh. No social upload or live-player deployment.

Actual male Kokoro80Puck20Fenrir1.02; listening acceptance UNVERIFIED.

0.000–2.062s: These two services can't finish starting.

2.142–5.668s: Spring starts Service A, whose constructor needs Service B.

5.748–12.840s: But Service B needs Service A first. The arguments must exist before construction. Neither constructor can finish.

12.920–18.568s: Startup fails with a bean currently in creation exception. This is a constructor cycle.

18.648–25.057s: Refactor the collaboration. An orchestration service calls A and B; they no longer depend on each other.

25.137–34.350s: Our tests confirm failure before, and successful startup after. Other circular references behave differently. Redesign the dependency graph.

36.350–37.441s: Thanks for watching.
