# Verification report — Constructor injection

**Production is INCOMPLETE for perceptual voice acceptance.** The actual narrated MP4 and its technical checks are finished. No listening, human naturalness, pronunciation, perceived-age, browser or physical-phone playback approval is claimed. The prepared mobile player remains unpublished pending manual approval.

Approved topic: **Constructor injection**. Publication: **2026-11-23**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The approved date and sequence are unchanged despite later production. No week/day/lesson/episode number appears in the media. No social upload, scheduling, thumbnail selection or live preview deployment occurred. Repository delivery follows the user's separate standing authorization.

## Actual encoded export

| Measurement | Actual result |
| --- | --- |
| Duration | 36.266667 seconds |
| Picture | Native 1080×1920, 9:16, H.264 High level4.2, progressive 8-bit yuv420p |
| Frames | 2176 frames; constant60/1 FPS; every timestamp checked |
| Audio | AAC-LC stereo,48000Hz; encoded stream 36.262s |
| Color | Rec.709 matrix, transfer and primaries; limited/tv range; SDR |
| Loudness | -15.86LUFS; -1.32dBTP; LRA3.1LU |
| Decode/black detection | Full decode exit0 with empty error log; no black intervals |
| Captions/scenes | 20 SRT cues, maximum41characters; seven scenes |

Master SHA-256: `1a48348ee337885b7d5fa73c4747368907b02e6bc353f0386a69fcfe6b7a2b10`.

FFprobe JSON, actual commands, stdout/stderr, frame timestamps and the completed render trace are retained in source/evidence. Fast-start MP4 metadata is enabled. No codec, rendering or test result is fabricated.

## Genuine Java/Spring verification

**2/2 actual JUnit tests passed**, with zero failures/errors. Main-source compilation, test-source compilation and JUnit all exited0 with empty stderr. The pinned stack is Spring/spring-test6.2.11, JUnit Jupiter5.12.2/platform1.12.2, JDK21.0.13 and ECJ3.40 targeting Java17. Eleven JARs have published-checksum verification, SHA-256 and license records. Five current Java source hashes match the executed sources. No standalone application/main execution or Spring Boot test is claimed.

Config imports the registered OrderService and DemoPaymentGateway components. OrderService has exactly one constructor and no constructor @Autowired. The context contains exactly one PaymentGateway candidate. Tests check constructor/annotation reflection, candidate count, injected-reference identity and service execution. placeOrder(2500) delegates to an in-memory gateway and returns demo-paid:2500. A separate manual-new control retains the caller-provided gateway, distinct from the context singleton. This does not imply injection into arbitrary objects created with new, a real payment or comprehensive application coverage.

Actual JUnit proof lines:

```text
constructors: 1
autowired: false
gateway same: true
order result: demo-paid:2500
manual uses caller: true
```

Six official Spring/JUnit pages returned HTTP200, with hashes and seven exact claim excerpts retained. Spring6.2.11's Autowired API verifies single-constructor selection without the annotation; the matching6.2 reference verifies the Spring4.3+ history. Import registration, context loading, getBean and assertSame references are also retained. Media validation checks this recorded execution and current source hashes; it does not pretend to rerun Java.

## Thumbnail and opening

The actual font is unmodified Inter Variable under SIL OFL, with source and hash in source/assets/inter-provenance.json. Its SHA-256 is `29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031`.

The headline uses Inter weight900, optical size32, at104/96/104px, white #FFFFFF. Lines are exactly “Spring Injection”, “No @Autowired?” and “It still works.” Only the middle line has the #0866FF blue background,20px radius and18/8px padding. The glyph union is X110..929/Y499..879; the highlight rectangle is X110..947/Y629..738. No stock portrait, copied creator asset, public numbering or decorative slogan is used.

Source frame0 **pixel-matches cover.png exactly**, including the separate full-hook caption. All headline words are visible immediately. Across61 source samples from0–1s the headline ROI is pixel-stable. The gateway-reference carrier starts moving at1/60s and produces51 distinct technical-background states. From1–2s the same constructor card moves into the explanation. The largest measured consecutive source transition delta is 3.677918 mean RGB levels; there is no fade to black or silent static introduction.

first-frame.png is decoded from the actual final MP4. Lossy decoded pixel identity is **not** claimed. Encoded frame0/source SSIM is0.998835; cover-versus-decoded mean RGB error is1.510544, with maximum local channel error117. Eight opening/transition samples have minimum SSIM0.997725. Actual0/.5/1/2s images and1.25/1.5/1.75s transition samples are retained in qa/.

Root viewed first-frame.png, the encoded opening contact, likely9:16/1:1/3:4 feed/profile crops, all seven decoded scenes, all six cut pairs and the actual last frame. Main text and code were readable in those small contacts, with no observed clipping or caption collision. Supporting technical labels are smaller. Faded layers during the code-card transition are intentional. Crop previews do not guarantee a platform's current crop or automatic thumbnail selection.

## Caption implementation and margins

Captions use Inter weight700, optical size32,52px, white #FFFFFF. Panels are black RGBA alpha209/255≈82%, rounded12px, with26px horizontal/14px vertical padding. Center is540/1380 and maximum padded width840px. There are one or two lines; text is wrapped rather than shrunk.

Pillow textbbox measures actual glyph bounds and RGBA alpha_composite produces the background. All20 cues passed padding, glyph and rectangle checks; different cue widths produce different panel widths. Nonblack-base pixel probes verify opacity, color and rounded corners. Source-underlay checks found no bright technical content beneath caption rectangles. Headline, technical opening ROI and caption region are disjoint. Every cue has3–6 whitespace words, with no karaoke, bouncing or flashing.

The opening caption is exactly “No Autowired? This still works.” from0–1.755125s. It is separate because the thumbnail headline has different words. Burned captions and the separate SRT match the final synthesis script, using sample-derived scene/edge boundaries and approximate20ms local-ASR word spans, not evenly divided estimates.

Source preflight sampled224 states and211 unique text bounds with zero violations. Final validation sampled251 source states and40 actual decoded states inside X90..990/Y250..1520. These are sampled visual checks, not manual inspection of every frame or a physical-phone test.

## Mechanism and ending

The animation shows the registered managed service, its sole constructor, parameter-type lookup, one matching candidate, the same gateway reference supplied through the constructor, field retention and service execution. It keeps caller ownership explicit for new objects. Config.class→Spring→Gateway→OrderService constructor→ready service is the completed overview.

Edit anchors include constructor3.34, parameter10.76, candidate12.88, supply15.10, stored reference18.02, ready19.04, call20.24, result22.14, verification25.25, manual scope27.02 and complete overview32.33s. These illustrate causality, not Spring/JUnit runtime performance.

The complete reading hold is **32.921167–34.921167s**, exactly2s before the separate spoken Thanks. All120 source core frames are identical;120 encoded frames were compared with minimum SSIM0.998044. The actual last frame2175 matches the expected Thanks state with SSIM0.999317.

## Audio and outstanding essential criterion

The actual local Kokoro v1.0 male voice blends80%am_puck/20%am_fenrir, at normal1.02 in seven coherent batches. One whole scene was regenerated to add the useful constructor-selection explanation. There is no slowdown, pitch shift, waveform stretching, word splicing or substitute TTS.

Clean narration is36.261917s,48kHz monoPCM24, SHA-256 `55029410b326510b359fccfb0dbfd556511b35ca08feddda25e7b256f45d4e48`. Source speech starts0.015021s; the hook finishes1.755125s. First2s encoded RMS is-16.41dBFS. Source peak is−1.514415dBFS with zero clipped samples and zero endpoints. Median voiced F0 is113.26Hz with4.63-semitone variation; these are measurements, not evidence of perceived age or human naturalness.

Unprompted small.en int8 ASR has83 normalized expected/86 observed tokens,6 edits and **7.2289% raw WER**. The literal script has82 whitespace tokens. Differences are compound spelling: Autowired→auto-wired twice and PaymentGateway→payment gateway. Three caption-only span merges use observed windows without inventing subword times. Raw transcript, score and word times remain unchanged; the ASR record matches the current WAV hash. G2P checks are not listening approval.

Ordinary joins are0.08s; longest pre-hold source quiet is0.519979s. Encoded silence detection finds only the closing tail at36.019979s. Original NumPy music/effects are ducked beneath speech and synchronized to reveals; two-pass normalization and full AAC decode/continuity evidence are retained. No third-party sampled music is used.

**Blocker:** no supported auditory-listening capability is available in this chat. Humanlike smoothness, pronunciation, rhythm, joins and perceived young-to-middle adult age have not received actual listening acceptance. The rendered Kokoro candidate is delivered, but production remains explicitly incomplete for this essential requirement. Automated ASR/G2P/pitch/signal checks do not replace it.

## Delivery, policy and manual approval

Both platform copies were independently probed and fully decoded with exit0/empty errors, and match the master byte for byte. Exact cover, first-frame, styles and SRT copies, platform manifests and ZIP CRC checks passed. The post-freeze delivery audit records final production-ZIP and manifest integrity rather than presuming it here.

Six official platform sources were actually consulted and hashed. platform-policy-review.md records current YouTube AI/monetization/Shorts-thumbnail and Meta AI/originality/Reels findings, with owner checks for current disclosure controls, manual cover/frame choice, crop/account notices and approval. Publishing text discloses AI narration. Neither automatic thumbnail selection nor monetization approval is guaranteed. Asset-rights and originality records preserve actual licenses and original script/graphics/NumPy-audio provenance without exhaustive global claims.

qa/mobile-player/dist/index.html and unchanged MP4/cover/SRT are prepared locally. Controls, inline source/download wiring, actual duration, JavaScript syntax and copied-media hash passed checks. **No Site is registered or published for this lesson.** Manual approval is required under the latest brief. Browser and physical-phone playback remain untested. Previous live lesson players are unchanged. Model binaries, environments, caches and bytecode are excluded; reproducible sources remain. Repository file delivery retains its separate standing authorization.
