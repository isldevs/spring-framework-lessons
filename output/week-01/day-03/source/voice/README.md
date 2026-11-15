# Local Kokoro male narration — constructor injection in Spring Boot

This production targets a younger-to-middle adult male explaining naturally and conversationally. That is a delivery target, not a verified biological age or an imitation of a named person. Subjective naturalness remains unverified because the runtime cannot ingest audio for listening review.

## Exact generation profile

- Kokoro v1.0 original float32 ONNX, local CPU inference through kokoro-onnx 0.6.1.
- Style embeddings:80% `am_puck` + 20%`am_fenrir`, both official American English male styles.
- Model inference speed **0.90**. This lesson uses calmer pacing than the earlier starting profile. No pitch shift or waveform time stretching was used;24 kHz model output is pitch-preservingly resampled to48 kHz.
- Seven complete utterances, each asserted to fit exactly one inference batch. The seven scene texts are preserved in generate.py and timing.json.
- Actual narration **35.819167s**,48 kHz mono PCM24. Its60 FPS video rounds to35.833333s.
- Explicit recap reading hold **32.283125–34.283125s**, exactly2s, before Thanks.
- Thanks card/audio scene **34.283125–35.819167s**, including350ms programmed tail.
- Quiet utterance-edge4ms fades prevent edit clicks. Native model sentence-ending decays remain; no artificial initial silence is added.

The main voice styles are blended before inference into a single style, not mixed as two simultaneous audio recordings. All model and voice bundle downloads are pinned by models.sha256 and rechecked in model-check.log. requirements-lock.txt pins the local inference/verification environment. Models and virtual environments are regenerated and excluded from Git/production ZIPs.

## Reproduction

From this directory:

```sh
./setup.sh
.venv/bin/python generate.py --speed 0.90 --voice am_puck80_fenrir20
.venv/bin/python qa.py --asr-model base.en
.venv/bin/python split_captions.py
```

Defaults match those commands. qa.py automatically invokes late_phrase_qa.py when full-stream ASR has omitted only the late separately synthesized Thanks utterance; it preserves the original full-stream score, requires an independently decoded actual audio crop to match, and stores separate provenance. It never fills missing words from the expected script silently.

The exact edit boundaries, all18display caption cues (maximum40characters), stage anchors and explicit reading-hold/Thanks intervals are in ../timing.json. Scene-ready and recap-complete animation timings are documented derived anchors, rather than invented spoken word boundaries.

## Rights evidence

The official model card declares Apache-2.0 and production/commercial deployment; both male styles are included in the same distribution, with no separate noncommercial restriction identified. The official voice table identifies am_puck and am_fenrir as male with target qualityB. This training-data estimate is not a naturalness acceptance test for this recording. The inference wrapper is MIT.

Saved evidence under licenses/ includes the official model card, male voice table, model release information, Kokoro Apache license and kokoro-onnx MIT license. No paid voice sample, external speech API or alternative TTS was used. Independent Whisper base.en is a verification-only MIT-licensed model and contributes no generated speech to the deliverable.

## Actual QA scope

Unprompted full-stream base.en recognizes the first74normalized words exactly but omits the3-word Thanks phrase after the deliberate reading pause. Raw WER remains **3.8961%**, three deletions of77expected words. A separate unprompted transcription of the actual Thanks audio crop recognizes all3words exactly. Combined observed timestamps cover the77words without altering the raw score. See asr.json, asr-summary.json, supplemental-asr.json and asr-alignment.json.

Source waveform has zero clipped samples, immediate15.81ms onset, varied pitch and quiet joins. Voice-qa.md records the measured source figures and limitations. These objective checks do not replace auditory listening acceptance for humanlike smoothness, intended age impression or subtle artifacts. No auditory approval is claimed.
