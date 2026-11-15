# Facebook Reels upload notes

Use `facebook-reels.mp4`. The video is 35.833333 seconds, native1080×1920,60FPS,H.264/AAC48kHz,Rec.709SDR, with local male Kokoro narration and burned English captions. The exact cover is embedded in the opening second, and the complete recap holds for two seconds before the Thanks card.

1. Select the MP4 for a Reel and paste the complete `caption.txt`, including its hashtags.
2. Use `cover.png` wherever custom cover upload is offered. If the interface only permits selecting an existing frame, choose a frame from the opening second; it displays this exact cover without a fade.
3. English captions are already in the picture. `subtitles.srt` is available separately where caption-track import is supported. Avoid a second automatic or decorative caption layer repeating the same words.
4. Review the actual upload preview for sound, crop, text and cover. Voice naturalness and perceived age have not been accepted by listening in this runtime. See `technical-checks.md` for current technical and voice-review status.

DemoGateway simulates an approval locally. The fake gateway belongs only to a separate service test. No real payment is processed and no payment API is called. No upload, scheduling or publication has been performed by this production workflow. Public copy contains no internal schedule or lesson numbering.

The closing recap connects Spring Boot startup, the PaymentGateway constructor requirement, the matching DemoGateway bean, reference injection and order placement. The completed diagram remains visible for at least two seconds.
