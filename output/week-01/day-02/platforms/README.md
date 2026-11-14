# Platform upload packages

Separate YouTube Shorts and Facebook Reels folders contain lossless copies of the same lesson master, its exact embedded opening cover, synchronized SRT, upload notes and paste-ready public copy. The production export is 35.650000 seconds, 1080×1920, 60 FPS, H.264/AAC stereo 48 kHz, Rec.709 SDR; the actual encoded values and validation are recorded separately in verification-report.md.

- youtube-shorts/: youtube-shorts.mp4, cover.png, subtitles.srt, title.txt, description.txt with hashtags, tags.txt, pinned-comment.txt, upload-notes.md, technical checks and checksum manifest.
- facebook-reels/: facebook-reels.mp4, cover.png, subtitles.srt, caption.txt with hashtags, upload-notes.md, technical checks and checksum manifest.

The opening cover is already part of the same MP4. Select an opening-second frame if a platform only supports choosing an existing frame for its thumbnail. English captions are burned in; the SRT is retained for accessible caption tracks rather than duplicate decorative captions.

The completed overview is held for two seconds before the brief Thanks for watching card. Voice naturalness and perceived age remain unverified by listening in this runtime. See ../verification-report.md for actual final measurements and outstanding acceptance limits. No platform upload, scheduling or publication is performed automatically.

Self-contained archives are day-02-youtube-shorts-upload.zip and day-02-facebook-reels-upload.zip, alongside day-02-production.zip under the parent week output folder. These unique names preserve the previous lesson's packages.
