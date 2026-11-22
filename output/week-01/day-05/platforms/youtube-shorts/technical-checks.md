# YouTube Shorts technical checks

**Export packaging complete. Technical validation passed. Perceptual voice acceptance remains unverified.**

- `youtube-shorts.mp4`: 39.300000s, native 1080×1920, 60 FPS, H.264 High, AAC stereo 48 kHz.
- Rec.709 matrix/transfer/primaries, limited range, yuv420p 8-bit SDR confirmed by actual FFprobe.
- Actual full decode exit 0, empty error log; 2358 video frames.
- Byte-identical lossless copy of the master. Video SHA-256: `3b882122e03afd42b9505b6e7f570741719c3704f86ca11b1453ee92584c9c83`.
- Immediate spoken and animated mechanism hook from frame one; separate branded cover PNG; burned English captions; separate SRT with 23 valid cues.
- Progressive closing recap, with completed diagram held for 2.00s before a separate Thanks for watching end card. User authorizes up to 45 s; this export stays strictly below 45 s.
- Encoded master loudness -15.89LUFS, true peak -1.37dBTP.
- Voice: local Kokoro 80% am_puck / 20% am_fenrir, adult male explanatory style. Independent base.en ASR: 97 expected words, raw normalized WER 0.000000; raw transcript and alignment provenance retained in production source. Raw speech-recognition evidence is retained without invented corrections.

No auditory listening review is claimed. Perceived age, human naturalness and subtle speech artifacts cannot be certified in this runtime. Final strict voice approval remains incomplete. All technical validation and packaging checks above are actual measurements, not a substitute for listening acceptance.

Use upload-notes.md and paste-ready copy. Caption overlays are already in the video; avoid duplicate decorative captions. Nothing has been uploaded, scheduled or published to YouTube or Facebook. All files in this folder except the manifest itself are covered by checksums.sha256.
