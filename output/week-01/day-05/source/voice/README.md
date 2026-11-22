# Local Kokoro narration — Bean naming

The actual delivered WAV uses Apache-2.0 Kokoro v1.0 and MIT kokoro-onnx inference. Male English styles are blended80%am_puck/20%am_fenrir. Model card, official male-voice table, release and license evidence are under licenses/. models.sha256 pins the model and voice files. Downloaded models, caches and environments are excluded from Git and delivery ZIPs.

All seven coherent scene utterances use model inference **1.02**, **0.08s ordinary joins**, a separate **2s complete-diagram hold**, and **0.25s final tail**. The user rejected0.80pacing on a prior lesson; this production never slows speech to fill runtime. The first normal-paced candidate lasted40.927500s. Only complete scene6 was shortened and regenerated, removing redundant wording and clarifying that this example's type tie remains unresolved by names. Other saved scene clips were retained without word-level splicing, pitch shifting or waveform time stretching. pacing-trials.json records the rejected duration.

Final narration is **39.286167s**,48000Hz mono PCM24. Picture rounds to **39.300000s /2358frames** at60FPS. The hook “Two names. One ambiguous type.” lasts1.787625s; its final recognized word ends1.400s. Speech begins0.015000s after file start. The hook refinement avoids implying that name changes alone solve or create type ambiguity. Visible alpha/beta beans share the Client type.

## Reproduce from the lesson directory

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
```

Literal inputs are in ../script-input.json. Each scene is one inference batch, with phonemes retained in pronunciation-g2p.json. The generator trims exterior quiet padding with a15ms consonant guard, resamples24→48kHz and uses4ms endpoint microfades. Optional --regenerate-scene replaces one complete scene only when the remaining source clips already exist. A full rebuild generates every utterance from the final script.

## Recognition and synchronization

Unprompted full-stream faster-whisper base.en int8, beam5, no initial prompt, recognizes **97expected/97recognized words**, edit distance0, WER0. Raw asr.json and asr-summary.json are preserved; no supplemental outro crop was needed. There are **23 captions**, maximum35characters. Names alpha/beta and Client require case formatting only. Optional look up/lookup compound alignment is supported, but this exact zero-WER transcript needs no such correction.

Known sample-derived utterance edits bound first/last cues; intermediate anchors use approximately20ms ASR words. Raw scores are never rewritten for alignment. Named and single-type lookup returns are0.30s after their requests; two-candidate failure is0.30s after its query. These are illustrative animation timings rather than framework benchmarks. The full recap holds **35.945417–37.945417s**, then separate Thanks continues to39.286167s. All absolute/relative events are in ../timing.json.

## Acceptance limit

No auditory listening review was performed: available tools expose no audio-ingestion capability. Intended younger-to-middle adult male age, smooth human naturalness, subtle artifacts and final pronunciation remain unverified by listening. ASR, pitch, silence and signal metrics do not establish those qualities. No fallback TTS, human approval or manufactured quality score is claimed. Final encoded audio and platform copies are checked separately by parent production.
