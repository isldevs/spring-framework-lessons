# iSLDevs production memory

These are the user's standing preferences and the decisions made while producing the Spring Framework lessons. Read this file together with `AGENTS.md` before starting a new video or revising one. Apply relevant defaults without asking the user to repeat settled instructions. A newer explicit user instruction takes precedence; a new topic replaces the lesson content, not the established production and delivery workflow.

## Destination and publication

- Repository: https://github.com/isldevs/spring-framework-lessons.git.
- After every generation or revision, finish and verify the actual artifacts, commit them with reproducible source, and push normally to the current branch. Report the resulting commit link. This is standing user authorization; do not ask for routine push confirmation again.
- Preserve existing lessons, unrelated work and Git history. Do not force-push.
- YouTube Shorts and Facebook Reels are the delivery targets. Prepare separate upload packages and platform copy. Never upload, schedule or publish to those platforms without separate explicit authorization.
- Keep virtual environments, bytecode, downloaded speech models and model caches out of Git. Retain dependency locks, download scripts, model hashes, licenses, source and verification evidence.

## Video specification and composition

- Deliver an actual finished native1080×1920 vertical MP4, H.264 video and AAC audio at48kHz, Rec.709 SDR, preferably60FPS. The current standard is60FPS.
- The user permits up to45seconds when explanation needs more time. Leave encoding headroom and keep exports strictly below45seconds. The original35–40second target is flexible; do not rush the explanation or remove useful diagram-reading time to force it shorter.
- Use5–7short scenes, including any closing card, with one purposeful progressive animation per scene. Show real mechanisms and reference/object flow rather than unrelated decorative boxes.
- Render graphics using Python/Pillow; use Manim or Blender only when necessary. Keep the production reproducible.
- Palette: dark navy, white text, cyan/purple/Spring-green accents; subtle iSLDevs branding.
- Keep important content inside X=90..990 and Y=250..1520. Inspect actual decoded frames at mobile size. Avoid clipped text, tiny code, crowding and unrequested footer slogans.
- Week/day/date identifiers are internal organization only. Do not show public lesson/day/episode numbering unless a newer request explicitly changes this.

## Opening cover is part of the same video

- Create a separate1080×1920 `cover.png` AND embed that exact cover as the opening frame of the final MP4.
- Display the cover from00:00 through approximately00:01, with no fade-in or black frames. The opening second must not add an overlay that changes the exact cover image.
- Begin narration immediately. Keep the cover within the safe region so it works as a thumbnail.
- This is important for phone uploads: when only an existing video frame can be selected as the thumbnail, the user can choose the first frame/opening second. A separate PNG alone is insufficient.

## Voice and audio

- Original, technically accurate English narration with a male AI delivery targeting a younger-to-middle-aged adult: smooth, conversational human explanation with clear technical pronunciation and deliberate pauses.
- Use a locally available, commercially permitted Kokoro male voice. The current working style is80%`am_puck`/20%`am_fenrir` at speed1.02. Treat that as a starting profile, not proof of perceived age or naturalness.
- Preserve coherent scene-level phrasing. Avoid unnecessarily splicing individual clauses; the working implementation uses one inference batch per scene where the model permits it. No artificial pitch shifting is needed to imply age.
- Review pronunciation, rhythm, pauses and naturalness where actual listening is available. Reject awkward/robotic delivery. Do not substitute another robotic TTS system if Kokoro fails.
- Do not claim an auditory review when the runtime cannot ingest audio. Automated ASR, pitch, clipping and silence checks support technical quality but do not establish perceived human naturalness. Clearly mark an essential unmet voice criterion incomplete.
- Use original quiet background audio and subtle effects synthesized with Python/NumPy. Duck music beneath speech; synchronize effects to meaningful events and preserve continuity through scene cuts.
- Deliver separate clean `narration.wav` and synchronized `subtitles.srt`. Captions must follow the actual narration; preserve raw ASR scores and document any alignment-only normalization.

## Clear technical explanation and closing sequence

- Write an original script with hook, mechanism, implication, concrete example, verification and takeaway as appropriate. Verify actual Java/Spring behavior and consult official documentation where relevant. Never fabricate code output or test results.
- A generic ending with a definitions box was unclear to the user. Make cause and effect concrete: identify who starts the action, what configuration/input is provided, which framework methods execute, what is created or wired, and what returns to the application.
- For Spring IoC, the useful explicit sequence is: the app creates `AnnotationConfigApplicationContext(Config.class)` as `ctx`; Spring reads `@Configuration class Config`; Spring invokes `@Bean Repo repo()` and `@Bean Service service(Repo repo)`; Repo is supplied to Service; the app later calls `ctx.getBean(Service.class)` on the same context and receives the ready Service reference.
- Distinguish startup/configuration/factory calls from later lookup. In the current non-lazy default-singleton example, objects are created during context startup and lookup does not invoke the factories again. Do not generalize that creation timing to every scope or lazy bean.
- Explain inversion of control without claiming Spring creates every Java object. Keep the registered/managed-beans qualification visible.
- Finish the explanation with a progressively revealed overview diagram. Hold the COMPLETE diagram for at least TWO SECONDS so viewers can inspect the whole mechanism.
- AFTER that reading hold, show a brief separate **Thanks for watching** card, with matching narration. Keep it inside the same MP4. Do not mistake the final two seconds of the movie for the diagram hold: the thanks card comes afterward.
- Check both the actual encoded recap hold and the actual last frame. Retain explicit `recap_hold_start/end/seconds` and thanks timing when applicable.

## Verification, rights and artifacts

- Use only free/open-source production software and commercially permitted assets. Preserve license/notices and document actual asset provenance. Do not claim exhaustive plagiarism screening or global novelty unless actually assessed.
- Inspect final MP4 streams with FFprobe; verify actual duration, resolution, FPS, codecs, audio rate and Rec.709 tags. Decode the complete file, inspect cover/closing frames and mobile readability, check audio continuity and compute SHA-256.
- Validate the master AND packaged copies. Preserve raw evidence, readable QA results and truthful remaining limitations. Refresh all manifests and ZIPs after changes; make reproduction shell scripts executable.
- Standard lesson location: `output/week-XX/day-XX/`. Keep the complete production ZIP and the two platform upload ZIPs alongside that folder under `output/week-XX/`.
- Retain video, cover, SRT, narration audio/script, timed storyboard, publishing metadata, tags, rights/originality records, QA/checksums, Java example, animation/audio source and reproducible dependencies. Standalone recap/thanks PNGs are useful supplementary deliverables.

## Required final response: links AND phone-copyable text

Follow the full mandatory checklist in `AGENTS.md`; do not shorten it to a video/ZIP link pair.

- Start with actual title, duration, resolution, FPS, video/audio codecs, audio sample rate, color space and verification status.
- Provide clickable download links for: MP4/complete ZIP; cover/SRT; narration audio/script; timed storyboard; YouTube metadata/hashtags/tags; Facebook metadata/hashtags; asset rights/originality review; QA report/SHA-256; both platform upload packages. Include the GitHub commit link.
- In that SAME response, also paste five separate copyable text blocks: YouTube title; YouTube description WITH hashtags; comma-separated YouTube tags; pinned comment; Facebook caption WITH hashtags.
- The user uploads from a phone. Metadata files or download links do NOT replace inline copyable publishing text. Include both formats every time a video is generated or updated.
- Never say completed/verified without identifying any remaining incomplete essential requirement.

## Current implemented reference

- Topic: What Is Spring IoC? Latest media revision: commit044ce2f4ef40c8fc66ff99a12ac5b410d20b498a.
- Master:43.416667seconds,1080×1920,60FPS,H.264/AAC48kHz,Rec.709; seven scenes and21SRT cues.
- Recap hold:39.962667–41.962667seconds; Thanks card follows. Cover remains in the opening second.
- Fresh Java ConfigFlowDemo traces startup, Config construction, factory calls before context readiness, then repeated singleton lookups with unchanged factory count. See `output/week-01/day-01/source/java/config-flow-notes.md`.
- Media source and QA: `output/week-01/day-01/`. All generated files and packages are already in GitHub history.
- Technical checks passed. Perceptual voice acceptance remains unverified because this runtime could not perform listening review. This is NOT a record of the voice having been auditorily approved.
- The complete final-handoff requirement was additionally saved in commit33d32efbe82a96dd482f00cebb2515b776dd2081. Read current AGENTS and this memory rather than relying only on past chat summaries.
