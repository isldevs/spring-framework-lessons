# Platform policy and manual publication review — Dependency resolution

Review date: 2026-11-27 UTC. This is a bounded review of the six official sources below, not a platform decision, legal clearance, account audit or promise of monetization. Publication remains manual and subject to the owner's approval. The approved proposed publication slot remains 2026-11-24 at 19:00 Asia/Phnom_Penh; this review does not reschedule it.

## Sources actually consulted

All six primary sources were freshly retrieved and returned HTTP 200. Actual final URLs, retrieval timestamps, response sizes/SHA-256, titles and short exact excerpts are retained in `source/evidence/policy-official-snapshots.json` and the per-source `policy-*.txt` records. Only brief excerpts and hashes are retained; full copyrighted policy HTML is not redistributed. `policy-fetch.py` reproduces the six captures. A follow-up text inspection verified the current upload-control and cover-selection wording rather than assuming that the preceding lesson's snapshot still applied.

| Official source | Applicable finding | Manual confirmation |
| --- | --- | --- |
| [YouTube GenAI disclosure](https://support.google.com/youtube/answer/14328491?hl=en) | Current guidance distinguishes realistic AI-generated/meaningfully altered content from non-realistic production assistance. The documented control is “AI use” under “Attributes.” Assess generated narration separately from schematic graphics. | Review the current AI use prompt and disclose when the realistic-AI definition applies. The intended natural-sounding Kokoro narration is AI-generated; do not call it human-recorded or assume all TTS is exempt. |
| [YouTube channel monetization](https://support.google.com/youtube/answer/1311392?hl=en) | Original educational substance and meaningful variation matter. Repetitive/low-value mass-produced or reused content can affect eligibility. Rights and monetization assessment are separate. | Confirm the channel/account's actual eligibility, rights and upload notices. Reusing templates alone does not establish originality or eligibility. |
| [YouTube Shorts creation and thumbnails](https://support.google.com/youtube/answer/10343433?hl=en) | The official app guidance documents choosing a video frame as a Shorts thumbnail, before or after upload; it distinguishes the YouTube app from Studio for this control. | Where the current app offers the frame picker, select the recognizable opening composition from 0–1 seconds, inspect its crop and save it manually. The encoded opening cannot force an automatic thumbnail choice. |
| [Meta 2026 AI disclosure statement](https://about.fb.com/news/2026/02/meta-prepares-for-2026-us-midterms/) | The official article reiterates disclosure/label-tool use for organic content with realistic-sounding digitally created/altered audio. The article's election context does not turn this Java lesson into a political advertisement. | Use the applicable AI info/self-disclosure control for realistic-sounding generated narration and confirm it before publication. A caption statement does not replace required native controls. |
| [Meta 2026 originality guidance](https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/) | Directly produced original content and substantive original value are favored. Duplicative uploads or minimal changes are not equivalent to original teaching. | Review the account/program's actual eligibility and originality notices. No recommendation, distribution or monetization approval is guaranteed. |
| [Meta Reels creation tutorial](https://business-auth.facebook.com/business/learn/lessons/what-are-fb-ig-reels) | The tutorial includes “Edit cover image,” primarily through Instagram steps alongside Facebook guidance. Current device/account interfaces can differ. | Confirm the actual Facebook/Business Suite cover control. Choose cover.png or the stable opening frame if supported and inspect feed/profile crops. No UI availability or automatic cover choice is guaranteed. |

## Application to this production

The production uses an original technical explanation, a controlled Spring dependency-resolution example with actual tests and observer trace, lesson-specific schematic animation and original NumPy audio. It does not reuse another creator's recording, portrait, thumbnail or finished video. The white/blue headline is a requested visual direction; composition and assets remain independently produced and licensed. A consistent iSLDevs identity and helper reuse do not remove the need for substantive educational variation across lessons. The rights and originality records establish provenance, rather than an exhaustive external originality verdict.

Narration is synthesized from licensed pretrained male Kokoro styles. It is not a human recording or a named person's imitation. Realistic-sounding synthetic audio must be assessed separately from the obviously schematic diagrams. The prepared description and caption state “Narration is AI-generated.” Confirm native disclosure controls independently; written disclosure does not replace a required platform setting.

## Required owner checks before approving publication

1. Listen to the final narration for naturalness, technical pronunciation and joins. ASR, G2P, pitch and signal checks cannot replace that acceptance.
2. Confirm current YouTube and Meta AI disclosure/self-label settings for the intended natural-sounding generated audio.
3. Select the opening thumbnail/cover manually where supported and inspect current feed/profile crops. Source/decoded cover similarity does not guarantee platform selection or crop behavior.
4. Confirm account/channel/program eligibility and any current copyright/originality/upload notices. No revenue or approval outcome is guaranteed.
5. Approve the final file, platform copy and publication action. No upload, schedule, live player deployment or social publication is performed by this editorial review.

Rights evidence is in `asset-rights.md`; encoded-media tests and production limitations belong in `verification-report.md`. Platform rules and app controls may change after this snapshot, so confirm the current upload interface before posting.
