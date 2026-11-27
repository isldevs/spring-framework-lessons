# Facebook Reels actual technical checks

**Technical media/copy validation passed. Perceptual voice acceptance remains a separate, unverified requirement unless an actual listening review is recorded.**

- `facebook-reels.mp4`: 37.033333s, native1080×1920,60FPS,H.264 High,AAC stereo48kHz.
- Actual FFprobe confirms Rec.709 matrix/transfer/primaries,limited-range,yuv420p8-bitSDR;2222frames.
- Actual full decode exit0,empty error log; SHA-256 matches master `6d02917cfc303376091b2b2f78604b1544d28a289dbdefe61745dc9263c3341e`.
- Source opening-frame/cover equality, headline stability/motion,1–2s transition and actual lossy-frame similarity are checked in production opening QA. No pixel-identical decoded/source-frame claim is made.
- Exact copied cover, decodedfirst-frame,SRT,styleJSON and policy record. SeparateSRT has18cues. Burned captions use the actual style record; no duplicate decorative captions are needed.
- Completed mechanism recap holds2.00s before separate spoken Thanks; duration stays strictly below45s.
- Encoded master loudness-15.86LUFS,truepeak-1.37dBTP.
- Local male Kokoro narration. Actual unprompted ASR modelfaster-whisper small.en int8 has77expectedwords and raw normalizedWER0.038961. Raw transcript and caption-alignment provenance are retained; recognition is not listening acceptance.

Three actual JUnit tests verify compatible-type discovery, exclusion of an unrelated same-named logger, autowire eligibility filtering, exact injected gateway identity, and missing/disabled-only candidate startup failures. The two expected refresh warnings belong to asserted negative tests. The pinned Spring6.2.11 implementation was inspected. No standalone application, business execution, payment, universal type-first resolution order or comprehensive behavior test is claimed.

Read upload-notes.md and platform-policy-review.md. Manual approval, cover selection, upload preview and current AI-disclosure confirmation remain user actions. No publication or monetization approval is guaranteed; no listening review is fabricated. This folder's manifest covers every file except itself.
