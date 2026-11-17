# Narration QA — pacing correction

## Current source measurements

- Local Kokoro v1.0,80%am_puck/20%am_fenrir male English styles; all7scenes one coherent batch at **1.02**. No pitch shifting, waveform stretching or substitute TTS.
- WAV **39.230750s**,48000Hz mono PCM24; frame-rounded picture **39.233333s/2354frames**.
- Hook utterance **1.461500s**; raw ASR final hook word **1.020s**. Signal above−60dBFS begins **0.015104s** and ends **38.964771s**.
- Peak **-1.514415dBFS**, RMS **-21.489852dBFS**, **0clipped samples**. Both endpoints are zero; quiet joins use4ms microfades.
- Voiced pYIN F0 10th/50th/90th percentiles **89.38/113.26/175.69Hz**; variation **4.64semitones**,2317voiced frames. These do not establish perceived age or human naturalness.
- Narration SHA-256: `f9047223934ffa400f270d86dc930cb477cbe29fba1bbfbad880ddae475d8e1d`.

## Independent recognition and caption provenance

Unprompted Whisper base.en int8, beam5, no initial prompt, produces **96expected/96recognized normalized words**, edit distance **0**, strict WER **0.000000**. This is a genuine fresh full-stream result. Raw transcript/timestamps and score remain preserved. Code-name display aliases (@Bean, @Component, FactoryConfig, lesson.scan) are documented separately without changing raw recognition.

There are **23 synchronized display cues**, maximum **37characters**. Exact utterance edits bound the first/last cues; intermediate anchors use approximately20ms ASR resolution. Known sample boundaries override raw boundary drift only. The original0.80 edition's72/73word,2.7778%classpath-spacing score is historical and is not the corrected audio's score.

## Pacing comparison and visual response

The user rejected the earlier slow delivery. Earlier body inference0.80 has been replaced by **1.02 throughout**. External scene joins dropped from0.18s to **0.08s** (with the old hook join0.12s); total inserted joins/hold/tail fell3.19→2.65s. The required2scomplete-overview hold remains intact. Useful script content increased72→96words, so the corrected video remains about39s while its overall script rate increases about112.5→146.8words/minute. Those are edit/script ratios, not listening judgments.

The prior source onset was already0.015104s. The reported delay was consistent with slow delivery, native-plus-inserted pauses and late visual reveals, rather than a seconds-long audio-track start offset. The corrected expected missing lookup follows request **1.6615s→1.9615s** (0.30s); Outside follows **23.020s→23.320s** (0.30s). Factory definition/call/Client/lookup anchors are **9.940/10.580/11.260/12.275667s**. They follow spoken keywords instead of waiting for the utterance's final word. These are explanatory animation anchors, not Spring execution timings.

Fresh source−45dBFS/120ms scan: longest pre-reading-hold quiet span **0.567250s**,20.117500–20.684750s. Complete recap hold is **35.890000–37.890000s**; Thanks begins afterward. Raw silence thresholds and intervals are retained in silence-scan.txt and silence-summary.json. The parent separately verifies encoded AAC loudness/continuity, final source/encoded correspondence and actual MP4 duration.

## Outstanding review

No auditory approval of the corrected version is claimed. This runtime cannot ingest the audio for listening. The user's feedback rejects the old pace; it does not establish acceptance of the new voice's human naturalness, pronunciation, subtle artifacts or perceived younger-to-middle adult age. Those essential criteria remain incomplete until actual listening review occurs. Objective ASR, pitch, silence and clipping metrics do not replace it.

Pinned model/voice provenance, licenses, locked dependencies, literal inputs and phonemes remain available. Model caches and virtual environments are excluded. No expected-transcript prompting, MOS surrogate or invented human approval is used.
