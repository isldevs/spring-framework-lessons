# Platform upload packages

Separate YouTube Shorts and Facebook Reels copies use the same rendered master, cover and synchronized captions with platform-specific filenames and paste-ready text. Actual stream properties and verification results are recorded in ../verification-report.md and each folder's technical-checks.md rather than inferred from these instructions.

The source timeline is 35.819167 seconds and the60FPS video rounds up to 35.833333seconds. It retains the exact cover in the first second, explains PaymentGateway constructor injection into OrderService, holds the complete recap for two seconds, then shows and says Thanks for watching.

- youtube-shorts/: youtube-shorts.mp4, cover.png, subtitles.srt, title.txt, description.txt with hashtags, tags.txt, pinned-comment.txt, upload-notes.md, technical/voice notes, FFprobe output and checksums.
- facebook-reels/: facebook-reels.mp4, cover.png, subtitles.srt, caption.txt with hashtags, upload-notes.md, technical/voice notes, FFprobe output and checksums.

Parent archives are day-03-youtube-shorts-upload.zip and day-03-facebook-reels-upload.zip; the complete source/delivery archive is day-03-production.zip. Unique names preserve earlier lessons.

The video already contains captions. Use the separate SRT for accessibility where supported, not as a second decorative caption overlay. The opening video frame can be selected as a thumbnail if the upload interface does not offer a separate custom-cover upload.

All approvals shown are simulations. No real transaction, payment API call, account upload, scheduling or platform publication is performed. Technical checks do not establish perceived voice age or smooth human naturalness; listening acceptance remains unverified in this runtime.
