# Facebook Reels technical checks

**Export packaging complete. Technical validation passed. Perceptual voice acceptance remains unverified.**

- `facebook-reels.mp4`: 35.650000s, native 1080×1920, 60 FPS, H.264 High, AAC stereo 48 kHz.
- Rec.709 matrix/transfer/primaries, limited range, yuv420p 8-bit SDR confirmed by actual FFprobe.
- Actual full decode exit 0, empty error log; 2139 video frames.
- Byte-identical lossless copy of the master. Video SHA-256: `5aa13ce8c9dab3ec4d24cb32a188cb495ef8632ba85752281a64c75b72cdfa28`.
- Exact supplied cover from 0–1 s; burned English captions; separate SRT with 16 valid cues.
- Progressive closing recap, with completed diagram held for 2.00s before a separate Thanks for watching end card. User authorizes up to 45 s; this export stays strictly below 45 s.
- Encoded master loudness -15.86LUFS, true peak -1.37dBTP.
- Voice: local Kokoro 80% am_puck / 20% am_fenrir, adult male explanatory style. Independent base.en ASR: 73 expected words, raw normalized WER 0.041096; raw transcript and alignment provenance retained in production source. The late Thanks phrase was also independently transcribed from its actual audio crop without a prompt and matched all three words; the raw full-stream omission remains recorded.

No auditory listening review is claimed. Perceived age, human naturalness and subtle speech artifacts cannot be certified in this runtime. Final strict voice approval remains incomplete. All technical validation and packaging checks above are actual measurements, not a substitute for listening acceptance.

Use upload-notes.md and paste-ready copy. Caption overlays are already in the video; avoid duplicate decorative captions. Nothing has been uploaded, scheduled or published to YouTube or Facebook. All files in this folder except the manifest itself are covered by checksums.sha256.
