# Verification report — Dependency resolution

**Production is INCOMPLETE for perceptual voice acceptance.** The narrated MP4 has been rendered and technically verified. Actual listening, pronunciation, smoothness and perceived-age acceptance remain unverified. No browser or physical-phone playback approval is claimed. The complete mobile player is prepared locally and remains unpublished pending manual approval.

Approved topic: **Dependency resolution**. Publication: **2026-11-24**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The approved date and sequence are unchanged despite later production. Internal week/day/episode numbering is absent from the public media. No social upload, scheduling, cover selection or live-player deployment occurred. Repository file/source delivery retains the user's separate standing authorization.

## Actual encoded export

| Measurement | Actual result |
| --- | --- |
| Duration | 37.033333 seconds |
| Picture | Native 1080×1920, 9:16; H.264 High, progressive 8-bit yuv420p |
| Frames | 2222 frames; constant 60/1 FPS; every timestamp checked |
| Audio | AAC-LC stereo, 48000 Hz; encoded audio stream 37.018s |
| Color | Rec.709 matrix, transfer and primaries; limited/tv range; SDR |
| Fast start | Actual moov atom at byte32, before mdat at byte60487 |
| Loudness | -15.86 LUFS; -1.37 dBTP; LRA 3.5 LU |
| Full decode / black detection | Exit0, empty decode error log; 0 black intervals |
| Captions / scenes | 18 SRT cues, maximum 40 characters; seven scenes |

Master SHA-256: `6d02917cfc303376091b2b2f78604b1544d28a289dbdefe61745dc9263c3341e`.

Actual FFprobe JSON, all frame timestamps, commands/stdout/stderr, render log and MP4 atom offsets are retained in source/evidence/. Source narration is37.017958s; the 60FPS export ceiling produces37.033333s without stretching speech.

## Genuine Java/Spring verification

**3/3 actual JUnit tests passed**, zero failures/errors/skips. Main compilation, test compilation and JUnit exit0. Compile stderr is empty. JUnit stderr contains two expected Spring refresh WARN messages from the asserted negative cases; an empty JUnit stderr is not claimed. No standalone application/main execution or real payment is claimed.

Pinned dependencies: Spring/spring-test6.2.11, JUnit Jupiter5.12.2/platform1.12.2, Micrometer1.15.4, ECJ3.40 targeting Java17; actual runtime JDK21.0.13. Eleven JARs have verified published checksums, hashes and retained licenses. Ten current Java source hashes match those executed.

SuccessConfig imports the Spring-managed OrderService. Its required single constructor requests PaymentGateway. The context registers eligibleGateway and backupGateway as compatible types; backupGateway has autowireCandidate=false. An unrelated AuditLogger is deliberately named gateway, matching the parameter name but not its type. Tests verify that the backup remains registered and explicitly retrievable, the unrelated bean is excluded, one eligible candidate remains, and the exact selected managed reference reaches OrderService.

A second fresh context has no PaymentGateway. A third has only the compatible but disabled backup. Both assert UnsatisfiedDependencyException with root NoSuchBeanDefinitionException and inactive context after failed refresh.

Actual stdout proof:

```text
compatible candidates: 2
eligible candidates: 1
unrelated ignored: true
gateway same: true
missing candidate: true
missing exception: NoSuchBeanDefinitionException
missing startup exception: UnsatisfiedDependencyException
disabled candidate missing: true
disabled compatible candidates: 1
disabled eligible candidates: 0
```

The observer-only TracingBeanFactory delegates decisions to Spring and records the actual successful dependency path: resolveDependency → compatible names [eligibleGateway, backupGateway] → true/false eligibility → [eligibleGateway]. This is runtime evidence for this controlled example, not a universal algorithm or performance benchmark.

Six exact Spring6.2.11 framework sources, their source JAR/hash and13 verbatim line excerpts are retained. Inspection covers doResolveDependency, findAutowireCandidates, eligibility and candidate selection. Spring6.2.11 also has a dependency-name shortcut requiring type compatibility and eligibility; qualifiers, primary settings and other branches can matter. The film therefore labels its path simplified and does not claim resolution always uses only names or types, or that this order applies universally. Six official Spring pages and seven claim excerpts were fetched/hash-checked. The media validator checks retained execution/source evidence; it does not pretend to rerun Java.

## Thumbnail, opening and decoded review

Inter Variable is unmodified under SIL OFL. Actual font SHA-256: `29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031`. Runtime axes: optical size32, weight900,104px for all three headline lines. Text is white; only Dependencies uses rounded#0866FF highlight, radius20, padding18/8px. Headline glyph union is X110..851/Y499..899; highlight is X110..869/Y793..907. The exact lines are How Spring / Finds Your / Dependencies.

Source frame0 pixel-equals cover.png, including the separate exact full-hook caption. Across61 samples0–1s the complete headline ROI remains stable. Meaningful type-request motion begins at1/60s and produces51 distinct technical states. From1–2s the same constructor code card moves into the dependency-request explanation; maximum consecutive source transition delta is 4.157679 mean RGB levels. There is no black frame, fade to black, silent static title card, greeting or logo intro.

first-frame.png is extracted from the actual encoded MP4. Lossy decoded pixel identity is not claimed. Frame0/source SSIM is 0.998942; mean RGB error is1.454871, maximum local channel difference122. Eight encoded opening/transition comparisons have minimum SSIM0.998288. Actual0/.5/1/2s and1.25/1.5/1.75s samples are retained in qa/.

Root visually inspected the actual first frame, opening contact, likely square/portrait feed crops, all seven scene stills, all six cut pairs and the actual last frame. Main headings, highlighted type, code and captions are readable in the inspected contacts. No clipping or caption collision was observed. Supporting framework metadata is smaller. Crop previews do not guarantee platform cropping or automatic thumbnail selection. qa/manual-visual-review.json records the actual scope; no every-frame or physical-phone viewing claim is made.

## Captions and safe margins

Inter weight700, optical size32,52px white text; measured black RGBA alpha209/255≈82%, rounded12px, horizontal/vertical padding26/14px, variable width≤840px, center540/1380, maximum2lines. Pillow textbbox measures actual glyph bounds; RGBA alpha_composite creates the panels. Different phrases produce different panel widths. All18 cues pass actual bounds, padding, glyph, alpha-color and rounded-corner checks. Source underlay probes found no bright technical content under the caption rectangles. All important content stays within X90..990/Y250..1520 in sampled checks.

The hook “How does Spring know what to inject?” is one exact cue0–1.604167s, balanced as How does Spring know / what to inject?. It remains separate because the thumbnail wording differs. All cues have3–7 words and match the known final synthesis text. Sample-derived phrase edges and observed local Whisper word spans supply synchronization, not evenly divided estimates. No karaoke, bouncing or flashing.

Source preflight: 224 states,223 unique text bounds, zero violations. Final safe-bound checks: 250 source states and44 decoded images. These are sampled visual checks; all2222 frame timestamps were checked separately.

## Mechanism and ending

The film illustrates the required PaymentGateway constructor parameter, compatible registered types, eligibility filtering, one selected managed reference supplied through the constructor and retained by OrderService. The backup is filtered from injection candidates, never deleted from the registry. The missing-dependency sequence explicitly creates a separate fresh MissingConfig context. It shows actual exception classes and no ready service after failure. Application business behavior and real payments are outside this example.

Narrated edit anchors include required type3.70, dependency descriptor5.02, compatible discovery8.24, unrelated exclusion9.82, eligibility13.54, unique candidate15.14, supply17.48, stored reference19.48, no candidate20.88, startup failure23.66 and test proof26.22s. These are editorial cues, not Spring wall-clock measurements.

The complete overview connects application register(SuccessConfig.class) / refresh() → BeanFactory → PaymentGateway matching and eligibility → OrderService(gateway), preserving the same managed reference and qualifier/primary caveat. It completes33.09s and holds **33.677208–35.677208s**, exactly2s before separate spoken Thanks. All120 source core frames are identical; all120 encoded hold frames were compared, minimum SSIM0.997400. Actual final frame2221 matches the expected Thanks state, SSIM0.999339.

## Audio and outstanding essential gate

Local Kokoro v1.0 male English blend80%am_puck/20%am_fenrir, normal1.02 speed, seven coherent scene batches,0.08s ordinary joins and0.25s closing tail. No time stretching, pitch shift, word splicing, substitute TTS or slowdown to fill runtime. Model/style/ASR hashes, licenses, dependency lock, phonemes, segments and actual inference logs are retained.

Clean narration:37.017958s,48kHz monoPCM24, SHA-256 `1ddc31b7429c55f54cc144f2d0ed0c7c42660d56f24f73c23058cfc345869d90`. Speech onset0.015125s; hook ends1.604167s. Encoded first2s RMS is-15.50dBFS. Source peak−1.514415dBFS, zero clipped samples and zero endpoints. Longest pre-hold source quiet interval0.5625s. Encoded silence detection finds only closing quiet from36.806042s. Original NumPy harmonic music and five effects are speech-ducked, synchronized and two-pass normalized. Full decode and objective continuity evidence are retained; no third-party music samples.

Unprompted faster-whisper small.en int8 has77 expected/78 observed words,3 edits, **3.8961% raw WER**. PaymentGateway→payment gateway is compound spelling; An unrelated→and unrelated remains pronunciation uncertainty. Caption-only known-input span mapping is explicit; raw transcript, score and times are unchanged and tied to the current WAV hash. Zero-duration Match and early Thanks ASR timestamps are documented, with sample-segment clamping and illustrative edit anchors rather than invented subword timing. G2P and measured pitch variation are not listening acceptance.

**Blocker:** no supported auditory-listening capability was available. Smooth humanlike delivery, terminology pronunciation, rhythm, joins and young-to-middle adult perceived age have not received actual listening acceptance. The real Kokoro candidate is delivered, but production remains incomplete for this essential quality requirement. A human must listen and approve, or awkward full utterances must be regenerated. Automated metrics cannot replace that review.

## Delivery, rights and manual approval

Both platform upload copies are independently probed, fully decoded and hashed after master verification; retained package evidence records exact outcomes. Finalization separately verifies all manifests, archive entries, CRCs and final byte hashes after reports/source freeze. Do not treat an archive's existence as proof of those checks.

Asset-rights/originality files preserve commercial-compatible input evidence without a guarantee of monetization or exhaustive global originality. Software license audit records actual Pillow MIT-CMU, NumPy/SciPy BSD metadata and FFmpeg/FFprobe GPL license output; font, Java and Kokoro/model licenses are separately retained. Six official YouTube/Meta policy sources were freshly retrieved on2026-11-27 with hashes and short excerpts. Current AI disclosure controls, account eligibility, manual frame/cover selection and cropping require owner confirmation. Platform text discloses AI narration. No automatic thumbnail selection or monetization approval is promised.

The mobile player qa/mobile-player/dist/ is fully prepared with native controls, inline playback markup and same-origin media/download links. Actual duration insertion, HTML/source wiring, JavaScript syntax and copied-media hash passed. **No Site was registered or deployed; no live player URL is invented.** Browser and physical-phone playback remain untested. Latest brief requires manual approval before publication/deployment; previous lesson players are unchanged. GitHub file/source delivery remains separately authorized. Model binaries, environments, caches, bytecode and symlinks are excluded from final delivery.
