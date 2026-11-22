# Actual narration QA — Bean naming

## Measured source

- Local Kokoro v1.0,80%am_puck/20%am_fenrir male English blend; all inference1.02, seven coherent batches. Only scene6 was regenerated as a whole to remove redundancy. No waveform stretching, pitch shift or word-level splice.
- **39.286167s**,48kHz mono PCM24; picture rounds to39.300000s/2358frames at60FPS.
- Signal above−60dBFS begins **0.015000s** and ends39.020813s. Peak **−1.514415dBFS**, RMS−20.549282dBFS, **0clipped samples**. Both endpoints are zero; quiet joins use4ms microfades.
- Voiced pYIN F0 percentiles10/50/90:87.34/113.26/169.71Hz; variation4.63semitones over2251voiced frames. These properties do not establish perceived age or human naturalness.

## Independent recognition and alignment

Unprompted full-stream Whisper base.en int8, beam5, no prompt, recognizes **97/97expected normalized words**, edit distance **0**, WER **0.000000**. Raw transcript, observed timestamps/probabilities and score remain under asr.json/asr-summary.json. No supplemental outro crop was needed; no expected words were inserted to manufacture a match.

There are **23 display cues**, maximum **35characters**. Alpha/beta/Client need only conventional case. Optional look up/lookup compound alignment is supported but not required in this transcript. Exact sample-derived utterance edits bound captions, while intermediate words use approximate20ms ASR resolution. Known edit bounds override timestamp drift only; alignment-normalization.json preserves provenance and raw scores.

## Pauses and illustrative events

The actual−45dBFS/120ms silence scan is retained in silence-scan.txt/silence-summary.json. Longest pre-hold quiet interval is **0.507896s**,28.543021–29.050917s. The deliberate2s overview hold is **35.945417–37.945417s**; the source quiet span35.504708–37.967500s includes native decay around that hold. Closing quiet tail38.902917–39.286167s lasts0.383250s at this threshold.

Registration name4.200s → definition4.300s → instance4.650s. Named request8.700s → reference9.000s; typed-name check11.920s. Single-type lookup15.700s → return16.000s. Fresh two-bean context registers beta18.940s → definition19.560s → instance19.910s. Query23.760s → two candidates23.860s → ambiguity24.060s. Named proof29.640s, type proof31.000s, takeaway32.220s and completed graph35.230s. These explain causal ordering, not Spring wall-clock performance. Parent renderer/media QA separately verifies actual frames and read windows.

## Outstanding essential review

**Auditory acceptance is INCOMPLETE.** This runtime has no audio-ingestion/listening capability. No listening approval is claimed for smooth human explanation, pronunciation, perceived younger-to-middle adult age or subtle synthesis artifacts. ASR/signal/pitch/pause metrics do not replace that acceptance. Actual licensed local male speech is delivered; no fallback TTS or invented MOS surrogate is used.

Model/voice hashes were actually rechecked successfully in model-check.log. The temporary model symlink is removed before delivery. Dependency locks, licenses, setup scripts, phonemes and source inputs reproduce the audio. Final AAC loudness/continuity and platform copies are parent-owned checks.
