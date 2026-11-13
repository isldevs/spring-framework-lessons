# Revised local Kokoro male narration

Delivery target: a younger to middle adult male explaining calmly and conversationally. This is a direction for the synthesized delivery, not a verified biological age or an impersonation of a real person.

The local voice style is **80% `am_puck` + 20% `am_fenrir`**, blended in the model's style embedding space. Both are official American English male Kokoro voices, each with target quality B in the official voice table. The blend uses no pitch shifting, resampling speed trick, or replacement TTS. Kokoro v1.0 float32 ONNX runs locally through kokoro-onnx 0.6.1 on CPU. Inference speed is 1.02. Actual narration: **44.367792 s**, 48 kHz mono 24-bit PCM.

The closing recap explains Define → Create and wire → Request and use. Production uses **six complete scene utterances**; the first five scene texts and timings are retained from the approved revision. Each whole scene is asserted to fit a single inference batch, so its sentences and clauses share one synthesis context without mid-scene edit splices. Punctuation guides breathing; 200–260 ms of additional separation is inserted between scenes, and a 2.0-second final diagram hold is added. Natural model sentence-ending decays contribute to measured pauses. Every scene edit uses a 4 ms quiet-edge microfade. No artificial initial silence is inserted.

## Reproduce

From this directory:

```sh
./setup.sh
.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20
.venv/bin/python qa.py --asr-model base.en
.venv/bin/python split_captions.py
```

Defaults match the shown arguments. `requirements-lock.txt` pins the inference and verification environment. `models.sha256` pins the main downloaded model and voice bundle. `generate.py` contains the exact blend, script, punctuation and pause settings. `segments/01.wav` through `06.wav` are the six scene-level synthesis sources. `../timing.json` records the exact spoken script, voice blend, scene edit boundaries, and 23 ASR-aligned display captions plus recap animation anchors. The published pronunciation of `getBean` is “get bean.”

`continuous=True` sliding synthesis is not used: this model distribution does not report durations, which that mode requires. The supported default path already synthesizes each of these short scene texts in one inference batch; `generate.py` asserts this explicitly.

## Actual automated review

Independent Whisper **base.en**, with no initial prompt, yields **102 expected words and 103 ASR tokens**, with raw word error rate **1.96%**. It recognizes the technical content but writes spoken “inversion” as two words, “in version,” in the final takeaway. Raw transcript and WER are retained unchanged in `asr.json` and `asr-summary.json`. For caption alignment only, `split_captions.py` documents and joins that one lexical boundary in `alignment-normalization.json`; no corrected 0-WER claim is made. Full scene G2P checks and distinct bean/being phonemes are preserved in `pronunciation-g2p.json`.

`../timing.json` includes `final_hold_start=42.367792`, `final_hold_seconds=2.0`, scene-relative `recap_cues`, and matching `recap_cues_absolute` derived from independent word timestamps. Those timestamps are approximate on a 20 ms grid.
Source clipping, onset, pitch variation, silence and joining checks are in `voice-qa.md` with raw metrics in `qa-metrics.json`, ASR output in `asr.json`, and the exact generation/QA logs. Current evidence describes this revised blend, not the superseded Michael narration.

## License evidence

- Official model card: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/README.md — declares Apache-2.0 and permits commercial deployment; saved in `licenses/Kokoro-82M-model-card.md`.
- Official voice table: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md — identifies `am_puck` and `am_fenrir` as male, target quality B, overall C+; saved in `licenses/Kokoro-82M-voices.md`. These grades describe training data, not acceptance of this specific synthesized delivery.
- Official project Apache 2.0 license: https://github.com/hexgrad/kokoro/blob/main/LICENSE — saved in `licenses/Kokoro-LICENSE.txt`.
- Model/voice release: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 — release information in `licenses/model-release.json`.
- Inference software MIT license: https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE — saved in `licenses/kokoro-onnx-LICENSE.txt`.

The official model distribution includes the voice style files under its Apache-2.0 model license; no separate noncommercial restriction appears in its model card or voice table. Both used voices are English. The original educational text and generated narration use no stock speech clips.

## Listening limitation

This runtime cannot ingest audio for a perceptual listening review. Automated recognition and prosody checks support intelligibility and varied delivery, but do not prove perceived age, smooth human naturalness, or absence of every synthesis artifact. The revised narration must receive listening acceptance before the strict naturalness requirement can be called complete. No perceptual listening is claimed.
