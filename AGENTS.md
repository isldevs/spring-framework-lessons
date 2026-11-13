# Lesson generation workflow

The user has authorized this repository as the destination for generated iSLDevs Spring lessons: https://github.com/isldevs/spring-framework-lessons.git.

- After every new lesson generation or regeneration, finish the actual deliverables, run the applicable verification, then commit and push the results to this repository on the current branch. This standing instruction does not require another routine push confirmation.
- Inspect the repository state first. Preserve unrelated work and existing lessons. Use a normal push; do not force-push or rewrite history. If the remote changed, integrate its changes before pushing. Report the resulting commit link.
- Store lesson deliverables and reproducible sources under `output/week-XX/day-XX/`. Keep associated platform upload ZIPs and the complete production ZIP alongside the lesson directory in `output/week-XX/`.
- Use a short progressive mechanism recap in the closing sequence. Reveal its parts with the narration, then hold the completed overview for at least two seconds so the audience can read it. Keep technically important boundaries and qualifications visible.
- Make recap flows concrete: show who starts the action, which configuration or input is read, which framework methods run, and which result returns. For Spring IoC, explicitly connect application startup with `Config.class`, invocation of its `@Bean` factory methods, dependency wiring, and later bean lookup; a generic definitions box alone was unclear to the user.
- Follow the completed recap reading hold with a brief “Thanks for watching” end card. Keep the recap hold before that card, rather than treating the final two seconds of the file as the diagram hold.
- The user permits videos up to 45 seconds when the explanation needs more time. Prioritize clear pacing and readable diagrams over forcing a lesson into 35–40 seconds; aim comfortably below the ceiling for encoding headroom. Do not remove useful recap reading time merely to meet a shorter target.
- Retain the finished MP4, exact opening cover, separate subtitles and narration, scripts, storyboard, platform metadata, rights/originality notes, QA evidence and SHA-256 manifests. Preserve the runnable Java example and animation/audio source.
- Exclude virtual environments, Python bytecode, model caches, downloaded binary speech models and large transient caches. Keep the model hashes, license evidence, dependency locks, download scripts and reproduction instructions needed to recreate those dependencies.
- Verify actual encoded files and packaged copies. Never fabricate Java output, test results or listening reviews. Keep any unmet quality requirement clearly documented; automated transcript or pitch checks do not establish human voice naturalness.
- Push to GitHub only. Do not upload, schedule or publish videos to YouTube or Facebook unless the user explicitly authorizes that separate action.
