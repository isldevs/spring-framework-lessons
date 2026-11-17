# Local Kokoro narration — corrected pacing

The delivered WAV is actual local Kokoro inference using80%am_puck/20%am_fenrir male English styles. The model distribution is Apache-2.0 and kokoro-onnx code is MIT; retained evidence is under licenses/. models.sha256 pins the model and voice bundle. Models, environments and caches are excluded from Git and delivery ZIPs.

## Pacing correction

The user reported that the previous voice sounded slow and delayed. That edition used body inference0.80 to fit the requested duration. Its audio onset was near0.015s, so it did not have a seconds-long initial track offset; slow delivery, stacked pauses and late reveal anchors made it feel delayed.

This edition uses **1.02 for all seven scenes**, **0.08s external scene joins**, an expanded useful explanation and earlier visual responses. It does not stretch or speed up an already generated waveform. Each scene is regenerated as one coherent inference batch. Keep the required2s overview-reading hold, but never slow speech merely to fill a target duration. A normal1.0–1.05 model pace is the starting range for future scripts.

Current narration is **39.230750s**,48kHz mono PCM24. Picture rounds to **39.233333s/2354frames at60FPS**. The hook utterance lasts **1.461500s** and its final recognized word ends1.020s. It starts immediately with the visible Client/missing-bean mechanism; no cover hold is inserted.

## Reproduce from the lesson directory

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
```

Literal inputs are in ../script-input.json. A full rebuild creates all seven coherent utterances. Optional --regenerate-scene can replace one complete scene only when the other saved clips already exist; the current correction regenerated all scenes. generate.py keeps native interior phrasing, trims only exterior quiet padding with a15ms consonant guard, resamples24→48kHz and applies4ms quiet-end microfades. No pitch shift or clause-level splicing is used.

## Recognition and synchronization

Fresh unprompted faster-whisper base.en int8, beam5 and no initial prompt, recognizes **96/96 normalized words**, edit distance0, WER0.000000. Raw asr.json and asr-summary.json are retained. Display names @Bean, @Component, FactoryConfig and lesson.scan correspond to spoken bean, component, Factory Config and lesson dot scan. Alignment merges their observed word spans without rewriting the raw transcript or score.

There are **23 display cues**, maximum37characters. Scene/caption boundaries use known sample-derived edits; intermediate words use approximately20ms ASR timing. Illustrative registration and lookup substeps are documented in alignment-normalization.json, not represented as runtime benchmarks. The missing lookup and Outside result reveal0.30s after their trigger cues. The complete overview holds **35.890000–37.890000s** before Thanks.

Earlier rejected pacing/recognition trials remain historical evidence. Their rates, word counts and scores are not the current result. Source signal, pitch, pause and SHA-256 evidence are summarized in voice-qa.md; final encoded audio is checked by the parent production.

## Acceptance limit

The user rejected the prior slow pacing. The production agent has not listened to this corrected version because the runtime has no audio-ingestion/listening capability. Human naturalness, final pronunciation, subtle artifacts and perceived younger-to-middle adult age therefore remain incomplete acceptance criteria. ASR, pitch and silence metrics are not substitutes for listening. No human approval or fallback TTS is claimed.
