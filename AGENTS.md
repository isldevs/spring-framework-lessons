# Lesson generation workflow

Before every new video or revision, read [MEMORY.md](MEMORY.md) for the consolidated production decisions and apply them alongside this file. New explicit user instructions override saved defaults.

The user has authorized this repository as the destination for generated iSLDevs Spring lessons: https://github.com/isldevs/spring-framework-lessons.git.

- After every new lesson generation or regeneration, finish the actual deliverables, run the applicable verification, then commit and push the results to this repository on the current branch. This standing instruction does not require another routine push confirmation.
- Inspect the repository state first. Preserve unrelated work and existing lessons. Use a normal push; do not force-push or rewrite history. If the remote changed, integrate its changes before pushing. Report the resulting commit link.
- Store lesson deliverables and reproducible sources under `output/week-XX/day-XX/`. Keep associated platform upload ZIPs and the complete production ZIP alongside the lesson directory in `output/week-XX/`.
- Use a short progressive mechanism recap in the closing sequence. Reveal its parts with the narration, then hold the completed overview for at least two seconds so the audience can read it. Keep technically important boundaries and qualifications visible.
- Make recap flows concrete: show who starts the action, which configuration or input is read, which framework methods run, and which result returns. For Spring IoC, explicitly connect application startup with `Config.class`, invocation of its `@Bean` factory methods, dependency wiring, and later bean lookup; a generic definitions box alone was unclear to the user.
- Follow the completed recap reading hold with a brief “Thanks for watching” end card. Keep the recap hold before that card, rather than treating the final two seconds of the file as the diagram hold.
- The user permits videos up to 45 seconds when the explanation needs more time. Prioritize clear pacing and readable diagrams over forcing a lesson into 35–40 seconds; aim comfortably below the ceiling for encoding headroom. Do not remove useful recap reading time merely to meet a shorter target.
- Preserve the exact approved curriculum topic and publication date. Approved Week 01 slots include ApplicationContext on 2026-11-17, Bean registration on 2026-11-18, Missing bean on 2026-11-19, Bean naming on 2026-11-20 and Multiple contexts on 2026-11-21, all proposed 19:00 Asia/Phnom_Penh. Keep week/day/episode numbering out of public media. Do not substitute another Spring topic for an approved slot.
- Follow the newest opening instruction. The current brief requires a spoken and animated mechanism hook from frame one, with a separate cover PNG and no static title/cover hold, greeting, fade or logo intro. This supersedes the older embedded-cover hold preference.
- Retain the finished MP4, separate branded cover, synchronized subtitles and narration, scripts, storyboard, platform metadata, rights/originality notes, QA evidence and SHA-256 manifests. Preserve the runnable Java example and animation/audio source.
- Exclude virtual environments, Python bytecode, model caches, downloaded binary speech models and large transient caches. Keep the model hashes, license evidence, dependency locks, download scripts and reproduction instructions needed to recreate those dependencies.
- Verify actual encoded files and packaged copies. Never fabricate Java output, test results or listening reviews. Keep any unmet quality requirement clearly documented; automated transcript or pitch checks do not establish human voice naturalness.
- The user rejected narration generated at0.80 as slow and delayed. Keep speech near normal conversational model pacing (about1.00–1.05); never slow it merely to fill the duration target. Add useful explanation when more runtime is needed, keep ordinary scene joins brief, and reveal visual results on the relevant spoken words rather than waiting for an utterance to finish.
- Push to GitHub only. Do not upload, schedule or publish videos to YouTube or Facebook unless the user explicitly authorizes that separate action.

## Required handoff after every video generation or update

This is the user's mandatory delivery format. A link-only or shortened handoff is insufficient.

1. Start with the actual video title, duration, resolution, FPS, video/audio codecs, audio sample rate, color space, and verification status. Report measured values and clearly identify any incomplete requirement. Never claim an unperformed check.
2. Provide direct clickable download links for every item below:
   - Finished MP4 and complete ZIP.
   - Cover and synchronized SRT subtitles.
   - Narration audio and narration script.
   - Timed storyboard.
   - YouTube metadata, hashtags, and tags.
   - Facebook metadata and hashtags.
   - Asset-rights record and originality review.
   - QA report and SHA-256 checksums.
   - YouTube Shorts and Facebook Reels upload packages.
3. In the same final response, paste all publishing text directly in chat, each field in its own copyable text block, because the user uploads from a phone:
   - YouTube title.
   - YouTube description with hashtags.
   - YouTube comma-separated tags.
   - YouTube pinned comment.
   - Facebook Reels caption with hashtags.
4. Do not substitute metadata download links for the inline copyable publishing text. Include both.
5. Push generated files and reproducible sources to https://github.com/isldevs/spring-framework-lessons.git, following the safe normal-push workflow above. Include the resulting GitHub commit link in the handoff.
6. Keep status truthful: completed rendering/packaging or automated checks do not establish perceptual listening acceptance. Disclose outstanding requirements without inventing results.
