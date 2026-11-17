# Bean registration — pacing correction and verification

**Corrected master and both platform copies: technical PASS. Overall auditory acceptance remains INCOMPLETE.** The user reported that the earlier version sounded slow and delayed. This revision regenerates the narration and retimes the animation; it does not claim a listening review that this runtime cannot perform.

## Why the earlier version felt delayed

The previous audio/video streams started at zero, and speech began after about15ms. The main problems were body narration generated at0.80 speed to fill the runtime, stacked scene pauses, and visual results revealed late. That pacing choice was a production mistake.

| Measured comparison | Earlier version | Corrected version |
| --- | --- | --- |
| Body model speed |0.80 |1.02 |
| Normalized spoken words |72 |96 |
| Words/minute across utterance spans, including native pauses |122.74 |157.46 |
| Added ordinary scene joins |0.84s total |0.40s total |
| Added joins + reading hold + final tail |3.19s |2.65s |
| Lookup request → missing result |2.504s |0.300s |
| Factory call reveal → Client instance |2.640s |0.680s |
| Outside class reveal → missing result |3.294s |0.300s |
| Required complete-recap reading hold |2.00s |2.00s |

The utterance word rate increases28.29%. The fuller explanation keeps the video near39s without deliberately dragging fewer words. These are arithmetic/signal measurements, not a certification of naturalness. Actual baseline records and a reproducible comparison are retained in `source/evidence/pacing-baseline.json`, `pacing-comparison.json` and `source/animation/pacing_comparison.py`. Earlier media remain in Git history at b2faf0913dcd5353af483db231b6a8bfe82ec00e.

## Approved lesson and publication plan

Topic **Bean registration**, publication date **2026-11-18**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC) are unchanged. Week/day identifiers remain internal. The video still opens with the spoken/animated question from frame one, uses a separate cover PNG and ends with the complete overview held for two seconds before Thanks. No social-platform upload, scheduling or publication occurred.

## Actual corrected encoded file

| Property | Measured value |
| --- | --- |
| Container/video duration | **39.233333s** |
| Picture | Native1080×1920, progressive H.264, yuv420p8-bit |
| Frame rate/count | Constant60FPS;2354decoded frames and2354timestamps checked |
| Color | Rec.709 matrix, transfer and primaries; limited range SDR |
| Audio | AAC stereo,48000Hz; stream duration39.231s |
| Clean narration |39.230750s,48000Hz mono PCM24 |
| Loudness | −15.89LUFS integrated, −1.22dBTP true peak,3.80LU range |
| Structure |7scenes;23SRT cues, maximum37characters |
| Full decode | Exit0 with empty FFmpeg error log |
| Black intervals |0detected with retained settings |

Master SHA-256:

```text
49d895bd36c7b93eb9bb6154f43a7320ea2689603b3ad90026f0e593f40d2d7f  video.mp4
```

All values come from the actual final MP4. The picture extends about2.6ms beyond the source audio to reach the next60FPS boundary, retaining the closing card. Raw FFprobe/commands/stdout/stderr, comparisons and hashes are in `source/evidence/final-*`; [final-summary.json](source/evidence/final-summary.json) is the machine record.

## Narration and subtitle checks

All seven coherent utterances use local licensed Kokoro80%am_puck/20%am_fenrir at **1.02** model inference. Ordinary inserted joins are **0.08s**, the complete-diagram hold is2s, and the final audio tail is0.25s. No waveform time stretching, pitch shifting or substitute TTS was used.

Raw unprompted full-stream Whisper base.en recognizes **96/96words**, edit distance0 and WER0. Raw ASR remains unchanged. Display formatting of FactoryConfig, lesson.scan, @Bean and @Component is documented separately; independently observed word spans are merged for those Java spellings. The23captions use exact sample-derived utterance boundaries and approximate20ms ASR word timing within each utterance. Known synthesis boundaries override boundary drift only.

Clean WAV onset above−60dBFS is **0.015104s**, peak−1.514415dBFS,0clipped samples and zero-valued endpoints. Voiced median F0 is113.26Hz, variation4.64semitones. The refreshed−45dBFS/120ms source silence scan finds the longest pre-hold quiet interval **0.567250s**, versus the previous0.675875s. The encoded−50dBFS/150ms scan detects only the intended closing quiet tail from39.061583s. Original quiet NumPy music/event cues remain ducked beneath speech; measured two-pass mixing and continuous audio are retained.

The updated word rate, zero transcript errors and signal metrics do not establish perceived age, human naturalness or every pronunciation detail. No auditory acceptance of this corrected version is claimed.

## Animation synchronization and readability

The failure panel now responds0.30s after the drawn request. The factory definition appears on the spoken bean-method phrase; the factory call follows “returns” and Client appears on its name, rather than waiting for a phrase-ending “result.” The Outside exclusion appears0.30s after that class is introduced. Three genuine closing proof lines now follow the narrated outcomes.

Current edit anchors: request1.6615/failure1.9615; registered factory configuration7.25225/definition9.94/call10.58/Client11.26/lookup12.275667; scan16.6/definition16.72/Worker17.0/complete graph17.35/lookup19.417292; Outside23.02/missing23.32. These are explanatory animation timings, not Spring execution benchmarks.

The production agent viewed actual decoded opening snapshots at0/.25/.5/1/2s, all seven scene stills, and before/after all six cuts at mobile scale. No clipped labels, caption collisions or crowded connections were observed. The opening core has113unique sampled frames and first changes at1/60s. Five encoded/source opening comparisons have minimum SSIM0.998607. All254source safe-bound samples pass X=90..990,Y=250..1520; a fresh217state preflight also passes.

The complete recap holds **35.89–37.89s** before separate Thanks. All120source hold samples are identical in the diagram crop; all120encoded comparisons pass with minimum SSIM0.998215. Actual last frame2353 matches the Thanks source with SSIM0.999186. See [visual review](source/evidence/visual-review.md). This is decoded-still and automated timing inspection, not continuous viewing on a physical phone or an auditory review.

## Java evidence retained and rechecked

The Java sources are unchanged. Their retained genuine verification has **3passing JUnit tests,0failures**, with main/test compilation, JUnit and standalone execution exit0 and empty stderr. This media revision checks that current source hashes equal that tested version and that the displayed outcome lines exist in its actual stdout; it does not claim a new Java run.

The tests verify an unregistered Client lookup in a refreshed context, a registered FactoryConfig/@Bean factory definition before instance/factory call, retrievable and reused Client, a configured component scan finding Worker, and annotated Outside excluded from lesson.scan. Both positive examples use separate contexts and default non-lazy singletons. Actual proof includes `plain class missing: true`, `@Bean retrieved: true`, `scan retrieved: true` and `outside scan missing: true`.

Actual retained toolchain: Spring6.2.11, JDK21.0.13, ECJ3.40.0 compiling Java17-target classes, JUnit Jupiter5.12.2 / console platform1.12.2,10pinned jars. No Boot, Maven or javac is claimed. [Java results](source/evidence/java-verification-result.json), XML/logs, hashes and runner remain reproducible. The earlier8official Spring pages and2publishing-link HTTP200 checks are retained; no new documentation fetch is claimed for this pacing-only revision.

Pictures show selected application definitions, not every infrastructure bean. The factory and configured scan are two valid registration paths; other APIs, including direct singleton registration, remain outside the focused example. The approved topic/date and publishing text are preserved.

## Packages, rights and remaining requirement

Both corrected platform copies were independently FFprobed and fully decoded with exit0 and empty error logs. Their2354frame MP4s are byte-identical to the corrected master SHA-256 above; covers/SRT match current assets. Separate platform manifests, metadata and phone-ready copy are retained. Upload ZIPs pass CRC checks; finalization also checks every production-ZIP member and refreshes archive hashes.

[Asset rights](asset-rights.md) and [originality review](originality-review.md) retain unchanged commercial-use provenance and review limits. Models/environments/Python bytecode are excluded; runnable Java, animation, audio/TTS sources, locks and license evidence are included.

**Remaining incomplete requirement:** actual auditory acceptance of smooth human explanation, pronunciation, perceived male age and subtle artifacts. The runtime cannot ingest the audio for listening review. The corrected media and technical checks are delivered, but overall strict approval remains incomplete for that reason. Nothing was uploaded, scheduled or published to YouTube or Facebook.
