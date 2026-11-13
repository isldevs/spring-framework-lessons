# Independent final artifact QA — closing recap revision

Technical checks PASS for the actual revised MP4. Final perceptual voice acceptance remains incomplete because this runtime cannot ingest audio for listening review. No perceived-age or human-naturalness approval is claimed.

Run `python source/animation/validate.py` from the lesson directory. It preserves actual commands, FFprobe JSON, stdout/stderr, frame timestamps, SSIM scores, decoded frames and safe-area samples under `source/evidence/final-*`.

## Actual encoded artifact

- MP4 duration **44.383333 s**, within the user's approved 45-second ceiling and strictly under 45 s. The source narration/edit timeline is 44.367792 s; frame rounding produces 2,663 video frames at constant 60/1 FPS.
- H.264 High, 1080 × 1920 progressive, yuv420p 8-bit SDR, BT.709 matrix/transfer/primaries, limited/TV range. AAC stereo, 48,000 Hz, encoded audio duration 44.368 s. The 15.333 ms video/audio duration difference is less than one 60 FPS frame.
- Full FFmpeg decode exits 0 with an empty error log. All 2,663 presentation timestamps begin at zero and increment by 1/60 s. No black intervals were detected.
- Encoded mix measures **−16.08 LUFS integrated**, **−1.31 dBTP**, and **4.00 LU** loudness range. A −50 dBFS silence scan with a 150 ms minimum finds only the intended final quiet/fade starting 44.076292 s; no internal silent interval occurs before the final reading hold. Decoder-reported quiet ends at 44.373333 s; the container/video ends at 44.383333 s.

## Cover, captions and mobile readability

- Source frames 0–59 are pixel-identical to the supplied cover, without a fade. All 60 decoded opening frames were compared against equivalent Rec.709-converted cover pixels: mean SSIM **0.998971**, minimum **0.998913**. Differences are normal lossy compression.
- All **23 SRT cues** have positive duration, remain ordered/non-overlapping and inside runtime, match the timing manifest within millisecond rounding, and preserve the actual narration words (including displayed `getBean` for spoken “get bean”). Rendering enforces at most two caption lines; no overflow occurred.
- **178 source samples** across opening frames, scene progress and caption intervals keep bright foreground pixels inside X=90..990/Y=250..1520. Background grid/glow is decorative and excluded from the brightness check.
- Six actual decoded scene frames were inspected at 360 × 640 phone scale. Headlines, code, graph nodes and captions are readable; no clipped or overlapping primary content was observed. The original first five scene branches and cover function are unchanged, documented in `recap-change-summary.json`; the normalized progress rail follows the new total duration.

## Closing recap review

The actual decoded final scene shows `@Bean definitions` registering with the Spring container, `Repo → Service` carrying the repository reference inside that boundary, an application `getBean(Service.class)` request pointing **up into the container**, and a green ready-service reference pointing **down to the application**. The qualifier **Managed beans only** remains visible. The already-created object graph precedes the request/return arrows, so the overview does not suggest that every lookup creates a new service or that the service calls getBean internally.

The recap's source edit interval is 29.250625–44.367792 s. Speech-aligned source anchors are retained in the timing manifest; the graph is fully assembled before the reserved final hold. The source reading hold is 42.367792–44.367792 s.

The final two seconds were tested independently using the completed diagram crop X=100..980/Y=534..1300, excluding captions and progress rail. **120 source crops are pixel-identical. All 120 actual encoded frames** of the corresponding final two-second crop match the complete reference with mean/minimum SSIM **0.998425**, above the 0.995 acceptance threshold. The final graph is stable long enough to inspect; this is an actual visual-content check rather than a duration label alone. Raw evidence is `final-recap-hold-ssim-*` and `final-recap-hold-reference.png`.

## Review limits

The existing actual Java execution evidence remains valid because the Java example and first five scene branches are unchanged. No new Java result was fabricated or claimed to have been rerun. The source narration's base.en recognition has 102 reference words/103 observed words and raw WER 1.9608%, attributable to the recognizer splitting “inversion” as “in version”; the raw transcript was retained. Caption alignment separately documents that word-boundary normalization. These checks do not establish voice naturalness and do not constitute auditory review.

This reviewer did not modify the final MP4, root verification report, platform packages, or checksum manifests.
