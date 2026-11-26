# YouTube Shorts actual technical checks

**Technical media/copy validation passed. Perceptual voice acceptance remains a separate, unverified requirement unless an actual listening review is recorded.**

- `youtube-shorts.mp4`: 36.266667s, native1080×1920,60FPS,H.264 High,AAC stereo48kHz.
- Actual FFprobe confirms Rec.709 matrix/transfer/primaries,limited-range,yuv420p8-bitSDR;2176frames.
- Actual full decode exit0,empty error log; SHA-256 matches master `1a48348ee337885b7d5fa73c4747368907b02e6bc353f0386a69fcfe6b7a2b10`.
- Source opening-frame/cover equality, headline stability/motion,1–2s transition and actual lossy-frame similarity are checked in production opening QA. No pixel-identical decoded/source-frame claim is made.
- Exact copied cover, decodedfirst-frame,SRT,styleJSON and policy record. SeparateSRT has20cues. Burned captions use the actual style record; no duplicate decorative captions are needed.
- Completed mechanism recap holds2.00s before separate spoken Thanks; duration stays strictly below45s.
- Encoded master loudness-15.86LUFS,truepeak-1.32dBTP.
- Local male Kokoro narration. Actual unprompted ASR modelfaster-whisper small.en int8 has83expectedwords and raw normalizedWER0.072289. Raw transcript and caption-alignment provenance are retained; recognition is not listening acceptance.

Two actual JUnit tests verify implicit single-constructor injection, the selected gateway reference, deterministic demo execution and manual caller-supplied dependencies. The demo performs no real payment. No standalone application or comprehensive behavior test is claimed.

Read upload-notes.md and platform-policy-review.md. Manual approval, cover selection, upload preview and current AI-disclosure confirmation remain user actions. No publication or monetization approval is guaranteed; no listening review is fabricated. This folder's manifest covers every file except itself.
