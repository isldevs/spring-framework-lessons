# Facebook Reels technical checks

**Export packaging complete. Technical validation passed. Perceptual voice acceptance remains unverified.**

- `facebook-reels.mp4`: 38.116667s, native 1080×1920, 60 FPS, H.264 High, AAC stereo 48 kHz.
- Rec.709 matrix/transfer/primaries, limited range, yuv420p 8-bit SDR confirmed by actual FFprobe.
- Actual full decode exit 0, empty error log; 2287 video frames.
- Byte-identical lossless copy of the master. Video SHA-256: `af155cc6dd42523d81b3297e2c2d3caa45739e0fddb54643480273524dd5a302`.
- Immediate spoken and animated mechanism hook from frame one; separate branded cover PNG; burned English captions; separate SRT with 22 valid cues.
- Progressive closing recap, with completed diagram held for 2.00s before a separate Thanks for watching end card. User authorizes up to 45 s; this export stays strictly below 45 s.
- Encoded master loudness -15.88LUFS, true peak -1.40dBTP.
- Voice: local Kokoro 80% am_puck / 20% am_fenrir, adult male explanatory style. Independent unprompted ASR: 91 expected words, raw normalized WER 0.021978; raw transcript and alignment provenance retained in production source. Raw speech-recognition evidence is retained without invented corrections.

No auditory listening review is claimed. Perceived age, human naturalness and subtle speech artifacts cannot be certified in this runtime. Final strict voice approval remains incomplete. All technical validation and packaging checks above are actual measurements, not a substitute for listening acceptance.

Use upload-notes.md and paste-ready copy. Caption overlays are already in the video; avoid duplicate decorative captions. Nothing has been uploaded, scheduled or published to YouTube or Facebook. All files in this folder except the manifest itself are covered by checksums.sha256.
