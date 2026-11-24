# Actual narration QA — Multiple contexts

## Measured source

Local Kokoro v1.0,80%`am_puck`/20%`am_fenrir` male English style blend, inference1.02 in every scene. Seven coherent utterances; the third was regenerated as a whole for an unambiguous context-label A pronunciation. No waveform stretching, pitch shifting, or individual-word splicing.

The source is **38.112500s**,48kHz mono PCM24. Signal above−60dBFS begins **0.014979s** and ends37.847146s. Peak **−1.514414dBFS**, RMS−20.423212dBFS, **0clipped samples**. Both endpoints are zero; joins retain4ms endpoint microfades.

Voiced pYIN F0 percentiles10/50/90 are87.34/115.24/175.69Hz, variation4.65semitones over2246voiced frames. These measurements do not establish perceived age or human naturalness.

## Pronunciation correction

Scene3 now begins `Context A finds alpha`. The original G2P read `A` as the indefinite article schwa. The generator records raw `kˈɑːntɛkst ɐ fˈaɪndz...` and uses `kˈɑːntɛkst ˈeɪ fˈaɪndz...` so the label is the letter A. The entire utterance is generated coherently after this precise phoneme override. Literal script, raw/used phonemes, speed and regenerated-scene metadata are retained. All other phonemes remain unchanged.

## Independent recognition and caption alignment

Final unprompted **faster-whisper small.en int8**, beam5, no prompt, recognizes **91words** against91expected tokens, with **2substitutions**, raw WER **0.02197802197802198 (2.1978%)**. The exact discrepancy is synthesis `The registries stay separate` recognized as `The registry stays separate`. Correct synthesis G2P contains plural registries and stay. No zero-error result or auditory acceptance is claimed.

Raw `asr.json` and `asr-summary.json` retain that transcript, approximate timestamps, word probabilities and honest error score. For display only, the two known synthesis labels `registries`/`stay` use the actual observed `registry`/`stays` spans; `asr-alignment.json` retains the unmodified recognized text and adds an explicit two-token alignment table. No word timing span is inserted. `alignment-normalization.json` documents this mapping. Caption text comes from the known synthesis script, rather than a claim that recognition heard those two words exactly.

There are **22synchronized display cues**, maximum **34characters**. Sample-derived scene/first/last-caption boundaries constrain ASR drift; intermediate words use approximately20ms recognition resolution. The complete hook utterance ends1.705292s and its last observed word ends1.36s.

The earlier superseded90-word base.en trial had4substitutions and is isolated under `trials/initial-90-word-pronunciation/`; it does not describe the final audio. The stronger final recognition is not presented as a listening review.

## Pauses and illustrative event timings

Actual−45dBFS/120ms silence evidence is preserved in `silence-scan.txt` and `silence-summary.json`. The longest quiet interval before the recap hold is **0.548875s**,8.365729–8.914604s. The deliberate diagram reading hold is **34.771750–36.771750s**; the larger measured quiet span34.259083–36.793833s includes native low-amplitude decay around that hold. The final source quiet tail37.729250–38.112500s is0.383250s at this threshold.

Observed registration words alpha2.66s/beta4.56s; isolated alpha result10.21s and beta-missing11.40s; parent set18.06s before child refresh19.06s; local check23.16s, parent fallback26.34s and reference return26.54s. Reverse lookup27.34s fails by28.62s. Verification begins29.54s, child-to-parent31.90s and parent-to-child33.06s; the complete overview state is cued34.63s before the exact2s hold. These are illustrative animation edit times, never measured Spring runtime performance.

## Outstanding essential review

**Auditory acceptance is INCOMPLETE.** No supported audio-ingestion/listening capability is available in this execution context. No listening approval is claimed for smooth human explanation, pronunciation, perceived younger-to-middle adult age, or subtle synthesis artifacts. ASR, G2P, signal, pitch and pause metrics cannot replace that acceptance. Actual licensed local male Kokoro speech is delivered; no fallback TTS or fabricated subjective quality score is used.

Kokoro model/style-bank hashes were actually checked successfully in `model-check.log`. The temporary model symlink is removed before handoff. Dependency locks, licenses, setup code, phoneme override and literal script inputs preserve reproduction. Final mixed AAC loudness/continuity and encoded frames/platform copies are verified by the parent production pipeline.
