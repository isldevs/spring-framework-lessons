# Facebook Reels technical checks

**Export packaging complete. Technical validation passed. Perceptual voice acceptance remains unverified.**

- `facebook-reels.mp4`: 44.383333s, native 1080×1920, 60 FPS, H.264 High, AAC stereo 48 kHz.
- Rec.709 matrix/transfer/primaries, limited range, yuv420p 8-bit SDR confirmed by actual FFprobe.
- Actual full decode exit 0, empty error log; 2663 video frames.
- Byte-identical lossless copy of the master. Video SHA-256: `bf2210acd945924d60504bb564904dae180e90ef73038106e4e4256d7e66f334`.
- Exact supplied cover from 0–1 s; burned English captions; separate SRT with 23 valid cues.
- Progressive closing recap, with completed diagram held for 2.00s. User authorizes up to 45 s; this export stays strictly below 45 s.
- Encoded master loudness -16.08LUFS, true peak -1.31dBTP.
- Voice: local Kokoro 80% am_puck / 20% am_fenrir, adult male explanatory style. Independent base.en ASR: 102 expected words, raw normalized WER 0.019608; raw transcript and alignment exceptions retained in production source.

No auditory listening review is claimed. Perceived age, human naturalness and subtle speech artifacts cannot be certified in this runtime. Final strict voice approval remains incomplete. All technical validation and packaging checks above are actual measurements, not a substitute for listening acceptance.

Use upload-notes.md and paste-ready copy. Caption overlays are already in the video; avoid duplicate decorative captions. Nothing has been uploaded, scheduled or published to YouTube or Facebook. All files in this folder except the manifest itself are covered by checksums.sha256.
