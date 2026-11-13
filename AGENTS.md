# Lesson generation workflow

The user has authorized this repository as the destination for generated iSLDevs Spring lessons: https://github.com/isldevs/spring-framework-lessons.git.

- After every new lesson generation or regeneration, finish the actual deliverables, run the applicable verification, then commit and push the results to this repository on the current branch. This standing instruction does not require another routine push confirmation.
- Inspect the repository state first. Preserve unrelated work and existing lessons. Use a normal push; do not force-push or rewrite history. If the remote changed, integrate its changes before pushing. Report the resulting commit link.
- Store lesson deliverables and reproducible sources under `output/week-XX/day-XX/`. Keep associated platform upload ZIPs and the complete production ZIP alongside the lesson directory in `output/week-XX/`.
- Retain the finished MP4, exact opening cover, separate subtitles and narration, scripts, storyboard, platform metadata, rights/originality notes, QA evidence and SHA-256 manifests. Preserve the runnable Java example and animation/audio source.
- Exclude virtual environments, Python bytecode, model caches, downloaded binary speech models and large transient caches. Keep the model hashes, license evidence, dependency locks, download scripts and reproduction instructions needed to recreate those dependencies.
- Verify actual encoded files and packaged copies. Never fabricate Java output, test results or listening reviews. Keep any unmet quality requirement clearly documented; automated transcript or pitch checks do not establish human voice naturalness.
- Push to GitHub only. Do not upload, schedule or publish videos to YouTube or Facebook unless the user explicitly authorizes that separate action.
