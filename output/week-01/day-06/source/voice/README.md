# Local male Kokoro narration — Multiple contexts

The literal approved narration lives in `../script-input.json`. Seven coherent utterances use a commercially permitted local Kokoro v1.0 model with an 80% `am_puck` / 20% `am_fenrir` male style blend, inference speed1.02 throughout, ordinary0.08s joins, a2s completed-diagram hold after scene6, and0.25s final tail. There is no waveform time stretching, pitch shifting or word-level splice.

## Reproduce

```sh
bash setup.sh
.venv/bin/python generate.py
.venv/bin/python qa.py --asr-model small.en
.venv/bin/python split_captions.py
```

The setup script downloads the Kokoro model/style bank and verifies the pinned SHA-256 values. Model binaries, virtual environments and recognition model caches are excluded from delivery. `requirements-lock.txt` records the installed environment; licenses/model cards and actual model hash checks are retained.

## Label pronunciation correction

The third utterance is `Context A finds alpha, but beta is missing. Sharing one Java application doesn't connect these registries.` Its initial standalone label `A` was interpreted as the English indefinite article by G2P. Adding `Context` alone still yielded schwa. The final generator explicitly changes that exact context-label phoneme from `ɐ` to `ˈeɪ`, preserving all approved words and synthesizing the ENTIRE scene as one coherent batch. `pronunciation-g2p.json` records the raw and actually used phoneme sequences. Other scenes reuse their original generated full-scene segments in this edit; a full reproduction generates every scene fresh at the same1.02 speed.

Final narration is38.1125s at48kHz mono PCM24. The complete diagram reading hold is34.77175–36.77175s; the separately spoken Thanks begins36.77175s. Picture frame rounding is handled by the renderer.

## Verification and scope

Final raw recognition, transcript, token timestamps/probabilities and honest word-error score are retained in `asr.json` and `asr-summary.json`; caption alignment must not replace the raw score. An earlier superseded90-word recognition trial is isolated under `trials/initial-90-word-pronunciation/`. Its results do not describe the final audio.

`qa-metrics.json` and `silence-summary.json` record actual signal, pitch and pause checks on the final waveform. Captions use known sample-derived utterance edits plus independent observed recognition word spans. The animation anchors derived from those spans are explanatory edit timings, never measured Spring performance.

**Auditory acceptance remains incomplete:** this execution context provides no supported audio-ingestion/listening capability. No human-smoothness, naturalness, perceived-age or pronunciation listening approval is claimed. Automated ASR, G2P, pitch, clipping and silence checks cannot establish that acceptance. Actual licensed male Kokoro speech is included; no substitute TTS was used.
