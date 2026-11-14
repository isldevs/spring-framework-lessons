# Local Kokoro narration — Spring dependency injection

Delivery target: younger-to-middle-aged adult male, calm and conversational. Perceived age and naturalness are not established by a preset name or numeric metric.

The narrator uses local Kokoro v1.0 float32 ONNX, kokoro-onnx 0.6.1, **80% am_puck / 20% am_fenrir**, speed **1.02**. Both styles are official American English male voices with target grade B. Style embeddings are blended before inference into one consistent voice, not overlaid recordings. No pitch shifting, waveform time stretching, external service or replacement TTS was used.

Seven complete scene utterances each fit a single inference batch, asserted before synthesis. Additional gaps are 180–220 ms, the completed-recap reading hold is exactly 2.0 s, and Thanks has a 350 ms final tail. Native decays add low-level quiet. Scene edits use 4 ms quiet-edge microfades. No artificial opening silence is inserted.

Actual clean narration: **35.649833 s, 48 kHz mono PCM24**. Source and scene timing are in `../../narration.wav` and `../timing.json`; seven before-normalization synthesis clips are in `segments/`.

## Reproduce

```sh
./setup.sh
.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20
.venv/bin/python qa.py --asr-model base.en
.venv/bin/python split_captions.py
```

The setup script downloads the production model and voice bundle, pinned by `models.sha256`; Python dependencies are locked. `qa.py` preserves the complete unprompted ASR transcript/score. If its only omission is the short final Thanks phrase, `late_phrase_qa.py` independently transcribes that actual audio crop without a prompt. It creates supplemental word timing only after an exact normalized phrase match; raw full-stream output and WER never change. Other mismatches stop alignment for inspection. `asr-alignment.json` records the actual timing provenance used for captions.

`split_captions.py` creates 16 display cues and scan/register/resolve/inject/use anchors. ASR word times are approximate on a 20 ms grid. The first Scan anchor uses the exact scene edit because ASR gave that word zero duration. Animation completion is a declared derived time, not a spoken-word observation.

## Licenses and review scope

Kokoro official model card declares Apache-2.0 and explicitly discusses commercial deployment. The official male voice table, Apache license, ONNX release metadata, and kokoro-onnx MIT license are retained in `licenses/`. No separate noncommercial restriction was identified for the two used male styles. Whisper base.en is a verification-only model and contributes no audio.

No auditory listening review is claimed. This runtime has not established audio-input support for judging human naturalness, age impression or subtle artifacts. Automated ASR/prosody checks cannot fulfill that perceptual acceptance. Actual metrics, the full-stream ASR omission and supplemental check are documented in `voice-qa.md`.
