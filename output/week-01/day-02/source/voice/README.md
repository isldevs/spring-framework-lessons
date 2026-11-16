# Local ApplicationContext narration

The actual delivered clean narration is `../../narration.wav`, generated locally using Kokoro v1.0 and an80% am_puck /20% am_fenrir male-style blend. Both styles come from the retained Apache-2.0 model distribution; kokoro-onnx inference code is MIT-licensed. Model card, voice table, project license and release evidence are retained in licenses/. Fixed model/voice download hashes are in models.sha256.

## Reproduce

From the lesson directory:

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 0.90 --hook-speed 1.00 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
```

The hook uses inference speed1.00; scenes2–7 use0.90. This is model inference pacing, not waveform stretching. Each scene is one coherent inference batch, with no word-level audio splices or pitch shifting. The original hook was shortened to “What’s inside ApplicationContext?” for spoken pacing; the technical topic stays unchanged. Public captions spell Java identifiers ApplicationContext/getBean while speech expands them naturally to application context/get bean. Both spelling transformations are recorded in alignment-normalization.json.

The model emits24kHz audio, resampled with polyphase filtering to48kHz PCM24. Only exterior quiet padding is trimmed, with a15ms guard and4ms endpoint microfades. A continuous original background mix is produced separately by the parent animation workflow. Intermediate scenes include short intended pauses; the complete recap has an exact2s reading hold before the separately spoken Thanks card.

The setup script recreates the locked voice environment and downloads checksum-pinned models. The production run used already cached local model files and the same locked dependencies; temporary model symlinks, environments and downloaded caches are excluded from Git/delivery. `candidates/` retains one rejected wording candidate with its own raw ASR evidence so it cannot be confused with final narration.

Final ASR and signal metrics are in asr*.json, qa-metrics.json, silence-summary.json and voice-qa.md. Raw scores are never silently rewritten. Caption edit points use known sample-derived utterance boundaries; intermediate word starts come from independent unprompted ASR. ASR word timing can drift across silence and is not phonetic ground truth.

**Essential review remains incomplete:** no audio-ingestion/listening capability is available here. Perceived younger-to-middle adult male age, smooth human naturalness and subtle synthesis/pronunciation artifacts require a real auditory review. Objective metrics are not listening approval; no such approval or MOS surrogate is claimed. No other TTS was substituted.
