# Local male Kokoro narration — Context smoke test

Literal final speech inputs live in `../script-input.json`. Seven coherent scene utterances use a commercially permitted local Kokoro v1.0 model, 80%am_puck/20%am_fenrir male style blend, normal inference1.02, ordinary0.08s joins, a2s reading hold after scene6 and0.25s final tail. There is no waveform time stretching, pitch shifting or individual-word splice.

## Reproduce

```sh
bash setup.sh
.venv/bin/python generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
.venv/bin/python qa.py --asr-model small.en
.venv/bin/python split_captions.py
```

The setup downloads and hash-checks the pinned Kokoro model/style bank; binaries, model caches and virtual environments are excluded from delivery. License/model-card evidence, hashes and dependency locks are retained. Fresh inference/PCM quantization may differ at the least significant sample bits; shipped-media checksums identify the actual delivered master.

## Actual edit and pronunciation

The original89-word candidate measured41.940083s. With root approval, two full scenes were shortened: required service lookup and the final scope/takeaway. The final78-word script measures36.985542s. Scenes3and6 were regenerated as coherent utterances at1.02; the other five reuse this lesson's original new scene recordings. They are not reused from an earlier lesson. `--regenerate-scenes 3,6` records that edit, while a full reproduction generates all seven scenes fresh.

No phoneme override was necessary. G2P pronounces JUnit as/dʒeɪ juːnɪt/, repository correctly, and both bean words as/bˈiːn/. These are input/phoneme checks, not a listening acceptance. Original and final script/timing evidence and old edited-scene recordings are retained in the isolated duration trial.

## Actual recognition and captions

Final unprompted faster-whisper small.en int8 is the primary recognition check:78expected/78observed words,6edits, rawWER7.6923%. It hears bean→being twice, expands they're→they are, and joins look up→lookup. The raw transcript, strict score, word spans/probabilities and current WAV hash remain unchanged.

Four caption-only transformations align the known synthesis script to the observed spans: two bean labels, a contraction span merge, and two look/up script labels sharing the observed compound span. They do not invent a subword boundary. The two bean differences remain recognition uncertainties; no human pronunciation approval is inferred from G2P. A separate bounded base.en comparison hears bean→beam twice and they're→there (3edits/3.8462%WER), retained as a crosscheck, not a replacement primary score or listening review.

Final captions contain20cues, maximum34characters. Sample-derived utterance boundaries constrain ASR drift, with intermediate word spans approximately20ms-grid estimates. The whole hook ends1.837792s; its last observed word ends1.68s. The complete recap reading hold is33.644792–35.644792s; spoken Thanks follows.

The final Load ASR token has zero duration at the compound lookup start. Only the illustrative diagram lookup reveal is staggered160ms after Load for readability: Load32.26/lookup32.42/assert32.64/complete33.17. Raw word times are untouched. These are explanatory edit cues, never Spring execution measurements. `alignment-normalization.json` and `timing.json` retain that derivation.

## Acceptance limitation

**Auditory acceptance remains INCOMPLETE.** This execution context offers no supported audio-ingestion/listening capability. No listening approval is claimed for naturalness, smooth human delivery, pronunciation, perceived younger-to-middle adult age or synthesis artifacts. ASR, G2P, pitch, pause and clipping metrics cannot replace that acceptance. Actual licensed local male Kokoro speech is delivered; no substitute TTS is used.
