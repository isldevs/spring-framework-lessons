# Narration QA — Spring dependency injection

## Actual source measurements

- Local Kokoro 80% am_puck / 20% am_fenrir, speed 1.02; seven single-batch scene utterances. No fallback TTS or pitch shifting.
- **35.649833 s**, 48 kHz mono PCM24; frame-rounded video duration **35.650000 s** at 60 FPS.
- Signal above −60 dBFS begins **0.016667 s** and ends **35.284458 s**. No artificial initial silence.
- Peak **-1.514415 dBFS**, RMS **-20.677608 dBFS**, **0 clipped samples**. Both endpoints zero; quiet joins have 4 ms microfades.
- pYIN voiced F0 10th/50th/90th percentiles **89.38/117.26/173.67 Hz**, variation **4.31 semitones** across 1990 voiced frames. This supports varied pitch, not perceived age or human naturalness.

## Independent recognition: preserve the actual omission

Unprompted Whisper base.en int8, beam 5, full-stream decoding recognizes the first 70 normalized words exactly but omits the three-word Thanks for watching after the deliberate recap hold. Raw result: **73 expected / 70 recognized**, edit distance **3**, normalized WER **0.041096 (4.1096%)**. Original `asr.json` and `asr-summary.json` remain unchanged. Do NOT report zero full-stream WER.

An independent, unprompted transcription of the real final audio crop **34.209083–35.649833 s** recognizes **Thanks for watching** exactly (3/3 words). `supplemental-asr.json` preserves this result and absolute word times. `asr-alignment.json` combines those independently observed final-phrase times with the untouched first-six-scene ASR. No expected words were silently inserted; the supplemental phrase had to match before alignment could continue.

Combined recognition covers all 73 expected normalized words. `alignment-normalization.json` records no text transformations and documents its timing sources. The exact script is retained in `../timing.json`. Captions total **16**, maximum **43 characters**. Word boundaries use an approximate 20 ms grid; source scene/hold edits are sample-derived.

## Rhythm and synchronization

At −45 dBFS / 120 ms, the longest non-hold internal quiet span is 0.606271 s at the verification-to-recap transition. The deliberate recap-to-Thanks quiet interval **31.820375–34.231167 s** lasts 2.410792 s, including native decay and the exact two-second reading hold. The final quiet tail **35.166583–35.649833 s** lasts 0.483250 s. Full log: `silence-scan.txt`.

The completed recap hold is **32.209083–34.209083 s**, followed by Thanks from **34.209083–35.649833 s**. Recap scan/register/resolve/inject/use anchors are **25.153958 / 25.42 / 25.92 / 26.38 / 27.56 s**. Scan uses the exact scene start because ASR gave its first word zero duration. Completion **28.21 s** is derived as 0.65 s after use; it is not claimed as an observed word boundary.

## Outstanding perceptual requirement

No auditory listening review was performed. The established runtime limitation prevents accepting smooth human delivery, perceived age or subtle synthesis artifacts. ASR, pitch, pauses and clipping metrics do not replace listening. Under the user's strict completion criterion, **voice naturalness acceptance remains incomplete**, despite the actual licensed Kokoro narration existing and passing the documented source checks.

No MOS estimator or transcript prompt was used as a substitute. Final mixed AAC loudness/continuity are checked separately by the production validator; these figures describe clean narration only. Models/voice hashes and license evidence are retained.
