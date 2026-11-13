# Current Config/Thanks final-file QA

Technical validation PASS. Actual master: 43.416667s, native1080×1920, H.264/AAC,60FPS,2605frames, BT.709 matrix/transfer/primaries with limited range. Full decode exit0 and empty error output. All presentation timestamps checked. No black intervals detected.

Encoded mix: -15.94LUFS, -1.38dBTP, 4.40LU loudness range. Only detected quiet tail begins at 43.228646s. Source narration has zero clipped samples; all99 normalized words match independent unprompted base.en ASR, raw normalized WER0.0. These are automated intelligibility/prosody checks, not listening acceptance.

All21 SRT cues are ordered, nonoverlapping, within runtime and word-equivalent to the exact seven-scene script. The main Thanks card supplies the spoken phrase on screen; the separate SRT still includes that cue. It is not duplicated in a second burned-in caption band.

First60 source frames are exact cover pixels, and all60 decoded opening frames match within compression tolerance: meanSSIM0.998971, min0.998913. The cover function and firstfive scene branches match the previous commit; see config-change-summary.json.

The complete Config diagram is held from 39.962667 to 41.962667s BEFORE the Thanks card. All120 source crops are identical. All120 actual encoded hold frames meet SSIM>.995; minimum0.997218, mean0.997248 CropX100..980/Y330..1310 includes the complete mechanism and qualifier, excluding captions/progress rail. Actual final encoded frame2604 matches the Thanks reference atSSIM0.998802, and the exact Thanks words match script/SRT.

Inspected actual decoded frames and mobile contact sheet: Config startup code, factory signatures, caller/parameter colors, later getBean request/return and closing Thanks are readable with no primary clipping observed. All192 source safety samples stay within X90..990/Y250..1520. Full constructor name36px, factory/lookup signatures38px, captions43px, closing Thanks88px. Core recipe headline62px. Low-level secondary labels are supplemented by narration.

Fresh actual Java trace independently confirms Config construction, both factory calls before context ready, and no extra factory calls during repeated getBean lookups. Compile/run exit0 with empty stderr; source/evidence/config-java-* preserves the evidence. Existing IoCDemo remains unchanged.

Earlier recap-* notes record the preceding generic ending. Current final-* and config-* evidence describes this revision. No auditory review was performed; perceived age, human naturalness and subtle synthesis artifacts remain UNVERIFIED. Nothing was published to YouTube/Facebook.
