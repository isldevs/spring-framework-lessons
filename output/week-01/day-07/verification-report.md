# Verification report — Context smoke test

**Actual narrated MP4 rendered and technically verified. Strict final approval remains INCOMPLETE: no perceptual listening acceptance is available.** Phone/browser playback also has not been tested here. No subjective naturalness, pronunciation or perceived-age approval is claimed.

Approved topic **Context smoke test**; publication **2026-11-22**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The date is preserved despite later production. No YouTube/Facebook upload, scheduling or publication occurred. Public media and publishing copy contain no week/day/episode numbering.

## Measured final MP4

| Check | Actual result |
| --- | --- |
| Duration/picture | 37.000000s; native1080×1920 |
| Frames/FPS | 2220 frames;60/1 constant FPS; all2220timestamps checked |
| Video | H.264 High, level4.2;8-bit yuv420p, progressive |
| Audio | AAC-LC stereo,48000Hz; encoded duration36.985s |
| Color | Rec.709 matrix/transfer/primaries; limited/tv range;SDR |
| Loudness | -15.92LUFS; true peak-1.34dBTP;LRA3.1LU |
| Captions/scenes | 20SRT cues,max34characters;7scenes |
| Full decode | Exit0,empty FFmpeg error log |
| Black detection | No black intervals detected |

Master SHA-256: `cddd6f1b3dd42e6e35d361e0300fb2d2482e12ec5424cb88be360e2999d99be1`. FFprobe JSON, real commands/stdout/stderr, all-frame timestamps and render trace are retained in `source/evidence/`. Rendering exited0; MP4 has fast-start metadata. No metadata/decoder result is invented.

## Actual Java and JUnit verification

Spring Framework and spring-test6.2.11; JUnit Jupiter5.12.2/platform1.12.2; JDK21.0.13; ECJ3.40 targetingJava17;11pinnedJARs with hashes/licenses. Main-source compilation, test-source compilation and actual JUnit execution each exited0 with empty stderr. **1/1 actual JUnit smoke test passed**, zero failures/errors/skips. No standalone application/main execution, Maven, javac or Spring Boot test execution is claimed.

`@SpringJUnitConfig(Config.class)` uses Spring TestContext support. JUnit creates the fixture; Spring support injects its `@Autowired ApplicationContext`. Selected Config defines default-singleton Repo and OrderService beans; its factory receives Repo and supplies it to the service constructor. The test retrieves both types, asserts non-null and calls `assertSame(repo, service.repository())`. It checks this expected reference relationship, not merely value equality. The framework owns context lifecycle; the example uses AFTER_CLASS DirtiesContext for demo cleanup and does not prescribe it for every test. Compatible contexts may be cached.

Exact real test stdout, emitted only after assertions passed:

```text
bean found: true
wiring same: true
```

Four source hashes, raw compilation/JUnit commands and logs, XML and dependency checksums match the tested sources. The media validator checks recorded proof/hashes without pretending to rerun Java. Six official pages were fetched with HTTP200 and hashed: Spring6.2.11 SpringJUnitConfig, SpringExtension, ContextConfiguration, DirtiesContext, BeanFactory, and JUnit5.12.2 Assertions. Eight exact claim excerpts are retained. The two publishing references were separately fetched and hashed.

This is a smoke test of the **selected configuration, required bean lookup and expected singleton wiring**. Order behavior, other configurations, unrelated/lazy beans and comprehensive application behavior are not established. No database/HTTP/business behavior test is claimed. The actual context's concrete implementation class is not asserted; visuals correctly say ApplicationContext.

## Actual visual and timing checks

Frame0 shows a ready managed graph and a pending expected-repository assertion. Source speech onset0.015104s; complete hook ends1.837792s; first2s encoded audio RMS-16.51dBFS. Core motion begins1/60s with50distinct opening states. Five decoded opening snapshots match source,minSSIM0.998805. There is no black/fade/static-cover delay. Separate cover is1080×1920.

Source preflight:217states,108unique text bounds,0violations. Final validation samples251source states and36decoded states with safe margins X90..990/Y250..1520. These are sampled checks, not manual every-frame review. Root inspected the actual encoded seven-scene contact sheet, all six transition pairs, five opening snapshots and actual final frame. Primary headings, lookup/assertion code, beans and captions are readable in the mobile-size contacts. Smaller type/configuration labels are supporting detail. No clipping or caption/diagram collision was observed in those stills.

The JUnit/test area stays outside the managed context. Repo is created before constructor wiring; required lookup returns the existing service reference; service and context references converge on one Repo. Actual JUnit result is revealed after the assertions, rather than falsely launching JUnit after they have run. Scope remains visible and the final diagram precedes Thanks.

Illustrative edit anchors: Config4.06; Repo6.8; constructor7.9; ready9.47; required lookup10.094/return11.59; expected Repo lookup15.58; identity assertion16.82/pass18.36; actual result reveal22.06. RecapLoad32.26/lookup32.42/assert32.64/complete33.17. The160ms recap stagger is a derived visual edit because raw ASR Load has zero duration; raw word times are unchanged. None of these edit times measures Spring/JUnit runtime performance.

Complete overview reading hold **33.644792–35.644792s**, exactly2s before separate spoken Thanks. All120source core frames are pixel-identical;120encoded hold frames compared,minSSIM0.998225. Actual last frame2219matches Thanks state,SSIM0.998810.

## Voice, captions, music and outstanding review

Actual local commercially permitted Kokoro v1.0 male80%am_puck/20%am_fenrir blend, normal1.02 in seven coherent scene batches. Root-approved concise edits regenerated two entire utterances; no pitch shift, waveform stretching, individual-word splicing or fallback TTS. Source is36.985542s/48kHz monoPCM24. SHA-256:`cbbedc48165a835978f87a82d162d72182ab52684a492f75fc9accae0f3080ff`. Peak-1.514415dBFS,0clipped,zero endpoints. F0median113.26Hz/std4.62semitones are measurements, not proof of perceived age/naturalness. Model/style-bank checks, licenses, locks, inputs and reproduction code are retained; no phoneme override was needed.

Primary unprompted small.en int8 ASR:78expected/78observed words,6edits, **7.6923% rawWER**. It recognizes two bean labels as being, expands they're to they are, and merges look up to lookup. Four explicitly documented caption-only transformations use observed spans; the compound shares its span without inventing subword timings and stays within one display cue. Raw transcript/score are untouched. A separate unprompted base.en comparison has3edits/78words,3.8462%WER, hearing bean as beam twice and they're as there. The recognizers leave the technical noun uncertain. Correct recorded synthesis G2P does not settle what a human hears; **no zero-error or auditory pronunciation acceptance is claimed**.

All20caption cues match the final78-word synthesis script. Sample-derived scene/first/last cue edges constrain approximate20ms ASR word timing; known alignment transforms and the zero-duration token are explicitly recorded. Ordinary scene joins0.08s; longest pre-hold source quiet0.593583s. Encoded silence detection finds only intended final tail beginning36.751521s. Original NumPy harmonic bed is ducked below narration, with5effects synchronized to matching reveals; two-pass loudness normalization and continuity/decode evidence are retained. No sampled third-party music.

**Essential incomplete criterion:** supported auditory listening/ingestion is unavailable. Smooth human explanation, pronunciation (including the uncertain bean noun), natural rhythm, perceived young-to-middle adult age and subtle synthesis artifacts have not received listening acceptance. ASR/G2P/pitch/pause/clipping checks cannot replace it. The actual narrated file is delivered with this limitation; it is not represented as fully voice-approved.

## Delivery and platform evidence

Owner-private phone player deployed successfully: https://isldevs-context-smoke-test-player.sivlayyi-bs.chatgpt.site . Native controls/playsinline and same-origin MP4/cover/SRT downloads use the unchanged master. Actual media hash, wiring/syntax/archive/source-remote checks, deployment/source IDs and access are in `source/mobile-preview/deployment.json`. Sign-in with the owner's ChatGPT account may be required. Browser/physical-phone playback was not tested because the managed browser tool was unavailable.

Both platform copies were independently FFprobed and fully decoded with empty error logs, and are byte-identical to the master. Exact cover/SRT, manifests and both upload ZIP CRC checks passed. Final lesson/archive manifests and complete production ZIP are generated only after source/report freeze; the parent `day-07-delivery-audit.json` records actual member/hash/CRC results. This report alone does not presume finalizer success.

Asset-rights/originality records retain actual software/font/model permissions and original script/graphics/audio provenance, without global novelty or exhaustive plagiarism claims. Java, animation, audio, voice and player sources are retained. Models, environments, bytecode and transient caches are excluded.
