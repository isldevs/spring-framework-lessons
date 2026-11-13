# Platform upload packages

Separate export packages are prepared for YouTube Shorts and Facebook Reels. They use the same approved animation and revised male Kokoro narration, with platform-specific filenames and text.

- `youtube-shorts/`: video, cover, SRT, title, description with hashtags, pinned comment and upload notes.
- `facebook-reels/`: video, cover, SRT, caption with hashtags and upload notes.

The final master passed technical validation: 36.916667 seconds, 1080 × 1920, 60 FPS, H.264/AAC, Rec.709 SDR, synchronized captions, no black frames or decode errors. Per-export validation and checksums accompany the packaged files. Export preparation does not certify how the voice will sound to a human listener. Perceived age and smooth naturalness remain unverified because this runtime cannot perform a listening review; see [the verification report](../verification-report.md).

The MP4 already includes captions. Separate SRT is retained for accessibility and compatible upload workflows; avoid duplicate on-screen caption layers. The exact cover is visible during the first second, so it can also be selected from the video if a custom cover upload is unavailable.

No upload, account changes, automatic scheduling or publication has been performed. Public text contains no internal schedule or lesson numbering.
