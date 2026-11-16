# iSLDevs production memory

These are the user's standing preferences and the decisions made while producing the Spring Framework lessons. Read this file together with `AGENTS.md` before starting a new video or revising one. Apply relevant defaults without asking the user to repeat settled instructions. A newer explicit user instruction takes precedence; a new topic replaces the lesson content, not the established production and delivery workflow.

## Destination and publication

- Repository: https://github.com/isldevs/spring-framework-lessons.git.
- After every generation or revision, finish and verify the actual artifacts, commit them with reproducible source, and push normally to the current branch. Report the resulting commit link. This is standing user authorization; do not ask for routine push confirmation again.
- Preserve existing lessons, unrelated work and Git history. Do not force-push.
- YouTube Shorts and Facebook Reels are the delivery targets. Prepare separate upload packages and platform copy. Never upload, schedule or publish to those platforms without separate explicit authorization.
- Keep virtual environments, bytecode, downloaded speech models and model caches out of Git. Retain dependency locks, download scripts, model hashes, licenses, source and verification evidence.

## Approved curriculum and schedule

- Preserve the curriculum exactly as supplied in each new production prompt. Never replace an approved lesson with an adjacent topic or move its publication date.
- The current approved slot is Week01 — Spring IoC Foundations, Day2 Tuesday: exact topic **ApplicationContext**, publish date **2026-11-17**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The proposed time remains a metadata field; do not automatically schedule or publish.
- The earlier generated How Spring Dependency Injection Works at day-02 was superseded by this explicit curriculum correction. Its media/source remain in Git history at d3040a5; the current day-02 directory must contain ApplicationContext.
- New explicit instructions take precedence over older lesson-specific visual defaults, including the previous static opening-cover hold.

## Video specification and composition

- Deliver an actual finished native1080×1920 vertical MP4, H.264 video and AAC audio at48kHz, Rec.709 SDR, preferably60FPS. The current standard is60FPS.
- The user permits up to45seconds when explanation needs more time. Leave encoding headroom and keep exports strictly below45seconds. The original35–40second target is flexible; do not rush the explanation or remove useful diagram-reading time to force it shorter.
- Use5–7short scenes, including any closing card, with one purposeful progressive animation per scene. Show real mechanisms and reference/object flow rather than unrelated decorative boxes.
- Render graphics using Python/Pillow; use Manim or Blender only when necessary. Keep the production reproducible.
- Palette: dark navy, white text, cyan/purple/Spring-green accents; subtle iSLDevs branding.
- Keep important content inside X=90..990 and Y=250..1520. Inspect actual decoded frames at mobile size. Avoid clipped text, tiny code, crowding and unrequested footer slogans.
- Week/day/date identifiers are internal organization only. Do not show public lesson/day/episode numbering unless a newer request explicitly changes this.

## Immediate hook and separate cover

- The latest approved brief requires an immediate visible and spoken technical hook at frame one. Start with a concrete mechanism and purposeful motion; no greeting, title-card hold, static cover hold, logo intro, fade-in or black frame.
- Create a separate1080×1920 branded `cover.png` inside the safe region. Keep this asset useful for platform cover upload without delaying the video hook.
- Inspect actual encoded opening frames and verify source narration onset. The first two seconds must communicate a clear question or surprising technical distinction.
- Earlier videos intentionally embedded an exact cover from0–1s for phone thumbnail selection. That is a historical implementation, superseded for the current brief by its explicit hook-first requirement. Follow any newer opening instructions supplied by the user.

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

## Latest implemented reference: ApplicationContext

- Approved exact topic ApplicationContext; current media/source at `output/week-01/day-02/`. Publication2026-11-17, proposed19:00Asia/Phnom_Penh (12:00UTC); no automatic upload/scheduling/publication.
- Actual master35.816667s,1080×1920,60FPS,H.264/AAC48kHz,Rec.709SDR,2149frames;7scenes and18SRT cues. Immediate animated/spoken hook “What's inside ApplicationContext?” replaces the older static-cover hold. A separatecoverPNG is delivered.
- Real Spring6.2.11 AnnotationConfigApplicationContext: no-arg creation → registerConfig → refresh (discover @Bean definitions, create default non-lazy Repo/Service) → getBean same wired Service → publishDemoEvent → close/singletoncleanup. BeanFactory area illustrates demo beans; infrastructure definitions already exist. Definitions remain distinct from created instances.
- Actual two JUnit tests pass: lifecycle/definitions-before-instances/wiring/identity/events/cleanup plus a separate @Lazy definition-without-instance contrast. Main/test compile, JUnit and standalone application exit0 with emptystderr. Pinned10jars, ECJ3.40 Java17-target, JDK21.0.13; no Boot/Maven/javac used. Exact proof same service:true/events handled:1/cleanup called:true.
- Animated applicationdefinitions11.460s, Service13.080s, completegraph13.430s, lookup15.260s, reference15.740s, event21.560s, close22.480s, cleanup23.480s. These are explanatory edit anchors, not Spring runtime measurements.
- Complete recap hold32.275958–34.275958s precedes Thanks. Actual encoded opening snapshots,6transitionpairs,7scene stills,120recapholdframes,lastframe andall2149timestamps were checked;249sourcebounds plus217preflightsamples pass.
- Male Kokoro80%am_puck/20%am_fenrir: hookinference1.00, remaining0.90,67/67rawunpromptedASRwords0WER. Rawoutrotimestampsdriftedintoquietreadinghold; finalcaptionusesknownsampleedit, withrawASR/provenanceretained. Listening acceptance is still INCOMPLETE; no perceivedage/humannaturalness approval claimed.
- CurrentmasterSHA25691335571e3011105f6aa29f8a8024ac3b4d6d929e9a547b7174cd9f32e0e7a9e. Bothplatformcopies independentlyprobe/decode/hashPASS andbyteidentical. Refreshallchecksums/ZIPsafterchanges. KeepmandatorydownloadlinksANDfivephonecopyblocks.

## Previous implemented reference: Constructor injection in Spring Boot

- Topic: Constructor Injection in Spring Boot. Source/media: `output/week-01/day-03/`.
- Actual master: 35.833333s,1080×1920,60FPS,H.264/AAC48kHz,Rec.709;7scenes,18SRT cues,2150frames. Exact cover source fills the opening second. Complete recap hold32.283125–34.283125s precedes the narrated Thanks card.
- Use real Spring Boot, not a bare context called Boot. This example runs non-web Spring Boot3.5.6 with Spring6.2.11. `@SpringBootApplication` scans `@Component DemoGateway` and `@Service OrderService`; the sole constructor requires the PaymentGateway interface and stores its reference in a final field with a null guard. No user @Bean factories are involved. A final reference is not object immutability.
- Two actual JUnit tests pass: real Boot startup verifies the sole managed gateway candidate, injected identity, construction-before-readiness/order, simulated receipt and singleton reuse; a separate pure Java test manually supplies a recording fake and verifies forwarding/call count/result. DemoGateway and the fake simulate payment outcomes; no real processor is contacted.
- Runtime is JDK21.0.13; the reproducible runner uses pinned ECJ3.40.0 to compile Java17-target classes without installed Maven or javac. Retain actual commands, exit codes, JUnit XML, aligned dependency hashes/BOM and license notices.
- The animation keeps PaymentGateway interface and DemoGateway object distinct. Constructor-ready anchor15.610s precedes application order use17.180s. The overview includes Boot startup/scanning, type matching, constructor requirement, supplied reference and later order use. These animation times are not runtime timings.
- This lesson's male Kokoro candidate uses80%am_puck/20%am_fenrir at inference speed0.90 to meet the duration target; this is a lesson-specific pace, not a universally approved voice setting. No waveform stretching or pitch shifting. Full-stream ASR74/77words,3.8961%WER; separate unprompted Thanks crop3/3. Preserve the raw omission and separate alignment provenance.
- Master and both platform copies passed actual probe, decode and hash checks;120encoded recap-hold frames and the actual last Thanks frame were compared. Perceptual voice acceptance remains unverified because no listening review was available. Do not treat automated metrics as humanlike-voice approval.
- Archives use day-03-prefixed names. Every handoff still requires all links AND five separate phone-copyable publishing blocks. Read newer explicit prompt requirements first; this lesson meets35–40seconds while retaining the requested reading hold.

## Superseded earlier revision: dependency injection in the Day 2 directory

- Earlier generated topic: How Spring Dependency Injection Works. Its35.65s media/source and actual component-scan/constructor verification remain in Git history at d3040a5d98ec5566a47c8337087d16cea9a30d73 under output/week-01/day-02.
- This revision has been replaced in the working directory by the explicitly approved ApplicationContext lesson. Do not describe current day-02 paths as the earlier DI topic or copy its static-cover opening into the current prompt.
- Prior actual verification and unaccepted listening status remain historical facts, not results for the new media.

## Previous implemented reference: Spring IoC

- Topic: What Is Spring IoC? Latest media revision: commit044ce2f4ef40c8fc66ff99a12ac5b410d20b498a.
- Master:43.416667seconds,1080×1920,60FPS,H.264/AAC48kHz,Rec.709; seven scenes and21SRT cues.
- Recap hold:39.962667–41.962667seconds; Thanks card follows. Cover remains in the opening second.
- Fresh Java ConfigFlowDemo traces startup, Config construction, factory calls before context readiness, then repeated singleton lookups with unchanged factory count. See `output/week-01/day-01/source/java/config-flow-notes.md`.
- Media source and QA: `output/week-01/day-01/`. All generated files and packages are already in GitHub history.
- Technical checks passed. Perceptual voice acceptance remains unverified because this runtime could not perform listening review. This is NOT a record of the voice having been auditorily approved.
- The complete final-handoff requirement was additionally saved in commit33d32efbe82a96dd482f00cebb2515b776dd2081. Read current AGENTS and this memory rather than relying only on past chat summaries.
