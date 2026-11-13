# Revised narration verification

Current voice: **80% local Kokoro `am_puck` + 20% `am_fenrir`**, both American English male, speed 1.02, CPU inference through kokoro-onnx 0.6.1. Delivery target is younger to middle adult, smooth explanatory speech. Perceived age and human naturalness cannot be certified by numeric metrics.

## Delivery revision

The former eleven short clause chunks have been replaced by six complete scene utterances. Each scene fits exactly one inference batch, asserted before synthesis. Punctuation and the model's continuous utterance context provide internal sentence phrasing; there are no mid-scene speech edits. No pitch shifting or substitute speech system was used. Quiet edit endpoints receive 4 ms microfades. Extra scene separation is 200–260 ms, with a programmed 450 ms final tail. Model-generated decays add silence around some sentence endings.

## Objective actual results

- Narration length **36.915542 s**, 48,000 Hz, mono, PCM 24-bit.
- First signal above −60 dBFS at **0.015250 s**. Immediate start with no artificial initial silence.
- Peak **−1.514415 dBFS**, RMS **−20.686998 dBFS**, **0 clipped samples**. Both endpoint samples are exactly zero; final mix loudness is handled by the renderer.
- Independent **Whisper base.en int8**, beam size 5, **no initial prompt**, recognizes all **88 words**. Normalized word error rate **0.0**. Singular bean, get bean and managed beans are recognized. Raw output is retained in `asr.json` and `asr-summary.json`.
- Diagnostic tiny.en initially substituted being for five singular instances of bean. The larger independent model resolves those correctly. This was a reason to check rather than silently correct the ASR. `pronunciation-g2p.json` records actual phonemes: bean `/bˈiːn/`, being `/bˈiːɪŋ/`, and get bean `/ɡɛt bˈiːn/`.
- pYIN voiced F0 10th/50th/90th percentiles: **87.34 / 112.61 / 173.67 Hz**; pitch variation **4.71 semitones standard deviation** across 2,292 voiced frames. The contour varies; this does not certify naturalness or age.
- Source silence scan at −45 dBFS with a 120 ms minimum: the longest internal quiet interval is **0.837562 s**, between the verification scene and takeaway. It spans the model's end-of-sentence decay and the designed scene gap. Other scene transitions contain about 0.37–0.74 s of low-level quiet. The longest within-scene sentence pause is approximately 0.326 s. The final quiet span is **0.868542 s**, including decay and the final tail. The word transcript is complete; no unexpected missing speech was detected. Full log: `silence-scan.txt`.
- Scene edit bounds are exact sample-based synthesis boundaries. The **18** display captions split at independent base.en word timestamps, which are approximate (20 ms grid). Every cue is at most 45 characters. `getBean` is the caption display for spoken “get bean.” Original exact narration is preserved in `../timing.json` under `phrases`.

## Perceptual acceptance remains blocked

The runtime does not support audio input for listening review. No auditory listening was performed or claimed. Automated checks show a complete intelligible transcript, varied pitch, deliberate pauses, and no clipping or long missing-speech dropout. They cannot establish that a listener perceives the voice as the requested age range or as smoothly human, nor exclude subtle synthesis artifacts. Listening acceptance is still required before calling the strict voice-quality requirement complete.

No noise MOS estimator or transcript prompt was used as a substitute for subjective listening.

## Reproduction

`./setup.sh`; `.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20`; `.venv/bin/python qa.py --asr-model base.en`; `.venv/bin/python split_captions.py`.

Model, voice bundle and software license evidence are retained in `licenses/`. Model/voice downloads are pinned by `models.sha256`; dependencies by `requirements-lock.txt`. Whisper base.en is a verification-only model and contributes no audio to the deliverable.
