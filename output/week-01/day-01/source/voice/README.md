# Local Kokoro Config explanation and thanks narration

Delivery target: one younger-to-middle adult American English male explaining conversationally. This is a synthesized delivery direction, not a verified biological age or an impersonation of a named person.

Voice style is **80% am_puck / 20% am_fenrir**, blended in model style space before local inference. Both are officially male Kokoro styles. Kokoro v1.0 float32 ONNX runs through kokoro-onnx 0.6.1, speed 1.02. There is no pitch shifting, waveform time stretching, external speech service or alternate TTS.

Actual narration: **43.403417 s**, 48 kHz mono 24-bit PCM. There are **seven complete scene utterances**, one inference batch each, without mid-scene edit splices. First-five-scene text and timing remain unchanged. Scene 6 explicitly connects app startup with Config, Config's bean methods, object creation/wiring, and later ready-service retrieval. Scene 7 says **“Thanks for watching.”**

The completed Config diagram's reading hold is **39.962667–41.962667 s**, exactly 2.0 seconds, at the end of scene 6. It is followed by the thanks card from **41.962667–43.403417 s**. The final350 ms is quiet tail. The hold is not the last two seconds of the whole clip. Metadata uses `recap_hold_start/end/seconds` and `thanks_start/end`, avoiding the previous misleading EOF-hold field names.

## Reproduce

```sh
./setup.sh
.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20
.venv/bin/python qa.py --asr-model base.en
.venv/bin/python split_captions.py
```

Defaults match these arguments. `requirements-lock.txt` pins installed packages; `models.sha256` pins the locally downloaded model and voice bundle. `segments/01.wav` through `07.wav` preserve the seven whole-scene source utterances before final peak normalization. Quiet edit boundaries have 4 ms microfades; no artificial initial silence is inserted. The supported inference path is asserted to fit one batch per scene; sliding `continuous=True` is unnecessary and unsupported by this model's lack of duration outputs.

## Actual automated checks

Independent Whisper **base.en**, int8, beam 5, without an initial prompt, recognizes **99 expected normalized words and 99 observed words**, edit distance 0, normalized WER **0.000000**. This includes Config, Config's, Repo, Service, bean terminology, and Thanks for watching. Raw transcription and metrics are retained in `asr.json` and `asr-summary.json`; this passing result is not a manual transcript correction. `alignment-normalization.json` is an empty list: no lexical substitutions or merges were needed.

There are **21 short caption cues**, at most 45 characters. Caption scene boundaries use exact synthesis edit positions. Internal splits use approximate ASR word timestamps on a 20 ms grid, which is quantization rather than an accuracy guarantee. The first caption of each scene is anchored to its known scene start, so the ASR's early timestamp for Thanks cannot intrude into the preceding diagram hold. Spoken “get bean” is displayed as `getBean`.

`../timing.json` records exact voice text, scene/hold/thanks timing and both relative and absolute overview anchors. Key anchors: Config load30.480s, Spring calls methods31.580s, creation33.180s, wiring34.440s, retrieval36.160s, ready36.880s, returned reference complete37.380s, managed-bean qualifier37.940s. Actual source Config/Repo/Service G2P phonemes are saved in `pronunciation-g2p.json`. They document inference inputs rather than substitute for listening.

Source peak/clipping, onset, pitch and silence details appear in `voice-qa.md`, `qa-metrics.json`, `silence-scan.txt`, and the exact generation/QA logs. The underlying model hashes were rechecked. Current evidence describes this Config/thanks revision, not the previous general recap.

## License evidence

- Official model card: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/README.md — declares Apache-2.0 and permits commercial deployment; saved in `licenses/Kokoro-82M-model-card.md`.
- Official voice table: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md — identifies `am_puck` and `am_fenrir` as male, target quality B, overall C+; saved in `licenses/Kokoro-82M-voices.md`. These grades describe training data, not acceptance of this specific synthesized delivery.
- Official project Apache 2.0 license: https://github.com/hexgrad/kokoro/blob/main/LICENSE — saved in `licenses/Kokoro-LICENSE.txt`.
- Model/voice release: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 — release information in `licenses/model-release.json`.
- Inference software MIT license: https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE — saved in `licenses/kokoro-onnx-LICENSE.txt`.

The official model distribution includes the voice style files under its Apache-2.0 model license; no separate noncommercial restriction appears in its model card or voice table. Both used voices are English. The original educational text and generated narration use no stock speech clips.

## Listening limitation

This runtime cannot ingest audio for a perceptual listening review. Automated recognition and prosody checks support intelligibility and varied delivery, but do not prove perceived age, smooth human naturalness, or absence of every synthesis artifact. The revised narration must receive listening acceptance before the strict naturalness requirement can be called complete. No perceptual listening is claimed.
