# Final artifact QA — How Spring Dependency Injection Works

**Technical QA PASS. Strict perceptual voice acceptance remains unverified.** No auditory listening review was performed; automatic transcript/pitch checks cannot establish perceived age, smooth human naturalness or absence of subtle synthesis artifacts.

## Actual encoded master

- Duration **35.650000 s**, within the newly requested35–40second target and strictly below45seconds. Video and AAC streams both report35.650000s.
- H.264 High, native1080×1920, progressive, yuv420p8-bit SDR, constant60FPS, **2139 actual decoded frames**. All2139presentation timestamps start atzero and increment by1/60s.
- AAC LC stereo48,000Hz. Rec.709 matrix, transfer and primaries plus limited/TV range are confirmed in this file's FFprobe output.
- Full FFmpeg decode exits0 with empty error output. Blackdetect reports no black intervals.
- Actual encoded audio measures **-15.86 LUFS**, **-1.37 dBTP**, **2.80 LU** loudness range. A −50dBFS/150ms silence scan finds only the intended final quiet tail beginning35.428792s. There is no internal silent dropout at those thresholds. The decoder's final tail extends to35.669333s due to normal AAC frame padding; the container/video duration remains35.650000s.
- Video SHA-256: `5aa13ce8c9dab3ec4d24cb32a188cb495ef8632ba85752281a64c75b72cdfa28`. The actual-file digest is retained in `final-video.sha256` and the summary.

## Cover, captions, safe bounds and mobile review

- Source frames0–59 are pixel-identical to `cover.png`, with no initial fade or caption overlay. All60decoded opening frames were compared with equivalent RGB-to-Rec.709 cover conversion: meanSSIM0.998915, minimum0.998874. Lossy differences are expected; the same supplied cover is visibly in the MP4 opening.
- All**16** actual SRT cues are ordered, nonoverlapping, positive-duration, within runtime and match source timing within0.51ms after millisecond rounding. Words match the seven-scene narration. The longest display cue has43characters, within the45character guard, and rendered captions use at most two lines.
- All**188** bright-foreground source samples remain within X90..990/Y250..1520. Decorative background grid may extend outside that region.
- Inspected all seven actual decoded scene samples in `final-decoded-mobile-contact.png` at360×640 phone scale. Headlines, core constructor/scan/lookup code, object names and captions are readable, with no visible primary clipping or crowding. Small configuration/status labels are supplemental to larger code and narration.
- Definitions are outlined and explicitly labelled metadata; runtime instances are filled. Configured package scanning, the Repo-type match, a Repo reference entering the service constructor, a ready graph, application lookup/use, recap and Thanks are visually distinct. No generic factory-method diagram from the previous IoC lesson was reused as this constructor-injection mechanism.

## Dependency graph exists before application use

The ASR-aligned renderer reports a ready dependency graph at**17.06s** and the application's use highlight at**22.84s**. The validator asserts both anchors lie in their respective scenes and the graph-ready anchor precedes use. Actual encoded snapshots at17.16s and22.94s were inspected:

- `final-graph-before-application-use.png` already shows Repo→OrderService with the service marked ready+wired.
- `final-application-use-start.png` shows application lookup and a returned wired reference; the existing graph remains present.

Java output independently verifies the mechanism and phase order, including definitions before construction and construction before application lookup/use:

```text
App starts Spring with Config.class
definitions registered: repo, orderService
Repo created
OrderService constructed with Repo
context ready
same Repo bean: true
application result: ready
scanned definitions: repo, orderService
```

This example has one unique Repo candidate and one service constructor; Spring uses that constructor without an `@Autowired` annotation. Its default non-lazy singleton graph is built during context startup. These observations do not claim all bean scopes instantiate eagerly, nor that scanning creates every Java object.

## Recap hold and actual last frame

The complete overview is held for exactly**2.0s**, from**32.209083 to34.209083s**, before the Thanks scene. All120source crops X100..980/Y330..1310 are pixel-identical. All120actual encoded hold frames were compared against the completed diagram: minimumSSIM0.998031, mean0.998094, both above0.995. Captions/progress rail are excluded from this diagram-stability comparison.

Thanks begins at34.209083s. Actual final encoded frame**2138** matches the Thanks source atSSIM**0.998781**. Script and separate SRT contain the exact phrase “Thanks for watching.” The main card itself displays these words; a duplicate lower caption band is intentionally suppressed.

## Narration evidence and limits

Local Kokoro is the licensed80%am_puck/20%am_fenrir male style at speed1.02, with scene-level coherent synthesis and no replacement TTS. Source voice metrics report zero clipped samples,16.67ms signal onset and varied pitch. The raw unprompted full-stream base.en transcription reports**70 recognized of73expected normalized words**, raw WER**4.1096%**. Its only three deletions are the short late Thanks phrase after the recap pause. A separate unprompted ASR pass on that actual audio segment recognizes all three Thanks words exactly; `supplemental-asr.json` preserves that result and its timestamps. The full-stream raw transcript/WER was not edited to claim zero. Main-body words and the supplementary ending cover the script, but this still does not constitute perceptual listening acceptance.

Reproduction: `python source/animation/validate.py`. Actual commands, stdout/stderr, FFprobe, all frame timestamps, per-frame SSIM scores and decoded PNGs are in `source/evidence/final-*`. No final MP4, parent verification report, publishing copy, archive or checksum manifest was changed by this QA task. No YouTube/Facebook upload or publication was performed.
