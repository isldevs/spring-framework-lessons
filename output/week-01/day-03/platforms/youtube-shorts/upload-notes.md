# YouTube Shorts upload notes

Approved topic: **Bean registration**. Publish date: **2026-11-18**. Proposed time: **19:00 Asia/Phnom_Penh (UTC+07:00;12:00 UTC)**. This plan does not schedule or publish anything.

1. Select `youtube-shorts.mp4` and paste title.txt, description.txt and optional comma-separated tags.txt into the corresponding fields. pinned-comment.txt supplies a comment to post and pin manually after publication if desired.
2. Upload `cover.png` wherever a separate custom cover is accepted. The video begins with the animated and spoken hook, without a static cover hold. If only a video frame can be selected, choose a clear opening mechanism frame.
3. Captions are already burned into the MP4. Retain subtitles.srt for accessibility where supported; avoid another overlapping automatic/decorative caption layer.
4. Review the actual platform preview for sound, crop, captions and hook. See technical-checks.md for measured export properties and voice-review limitations. Human naturalness, pronunciation and perceived age have not been auditorily approved in this runtime.
5. The closing recap shows registered factory configuration and configured component scanning leading to managed beans. It holds complete for two seconds before the separate Thanks card.

The two registration examples use separate contexts and default non-lazy singletons. @Component must be discovered or explicitly registered; an annotation alone does not activate a package scan. Public copy has no week/day/episode numbering. No account upload, scheduling or publication has been performed.
