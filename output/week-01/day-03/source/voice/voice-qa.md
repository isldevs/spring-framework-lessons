# Narration QA — Bean registration

## Delivered source and measured signal

- Local Kokoro v1.0,80%am_puck/20%am_fenrir male English blend; one coherent batch per scene. Hook inference1.00, body0.80. No pitch shifting, waveform stretching or substitute TTS.
- WAV **38.387208s**,48000Hz mono PCM24. Frame-rounded video **38.400000s /2304frames**.
- Hook utterance **1.486333s**; raw ASR recognizes its final bean word by **1.040s**. Source signal above−60dBFS begins **0.015104s** and ends **37.998396s**.
- Peak **−1.514415dBFS**, RMS **−20.434558dBFS**, **0clipped samples**. Both waveform endpoints are zero; quiet joins use4ms microfades.
- Voiced pYIN F0 10th/50th/90th percentiles **92.53/115.24/162.98Hz**; variation **3.88semitones**,2127voiced frames. These are objective signal properties, not proof of perceived age or human naturalness.
- Narration SHA-256: `d790098c38e089af4ae0522e9b34b9ca9f1baaee3c32884f85bc103859e633a7`.

## Final independent recognition and caption provenance

Unprompted Whisper base.en int8, beam5, without an initial prompt, produces **72expected /73recognized words**, edit distance **2**, strict normalized WER **0.0277778 (2.7778%)**. The only mismatch is **classpath → class path**. The full raw transcript and score remain in `asr.json` / `asr-summary.json`; do not claim zero full-stream WER.

Caption alignment explicitly merges the independently recognized class/path timing spans into the technical compound classpath, preserving their actual boundaries. `@Bean` and `@Component` are the displayed Java annotation spellings of spoken bean and component; punctuation is omitted for token comparison. No expected words were inserted. The final Thanks phrase is present in the unprompted full stream; `supplemental-asr.json` records that no additional crop was required. First/last display cue boundaries follow known sample-derived synthesis edits rather than allowing raw ASR drift into the preceding quiet hold.

The final scanning phrase was regenerated after both full-stream and independent crop recognition heard the original class-as sequence as class's. Parent-approved rewording removes that ambiguity. Rejected original-phrase evidence is retained only under `trials/`. The initial0.95-body candidate was rejected because30.733292s was below the target; neither rejection is represented as an auditory naturalness judgment.

There are **18synchronized display cues**, maximum **35characters**. Word times have approximately20ms ASR resolution; scene cuts and silence inserts are sample-derived. Factory/scanning registration, creation and lookup anchors include documented illustrative offsets, not runtime benchmark timings.

## Pauses and continuity scope

The source−45dBFS/120ms scan finds the longest pre-reading-hold quiet interval **0.675875s**,16.275958–16.951833s, between scene phrases. The recap-to-Thanks quiet span34.264083–36.745125s lasts2.481042s, including natural decay and the exact2s inserted reading hold. The final quiet tail37.888500–38.387208s lasts0.498708s. Raw thresholds and intervals are retained in `silence-scan.txt` and `silence-summary.json`.

Complete recap hold: **34.679125–36.679125s**. Thanks begins only afterward. Factory definition12.160s, factory call12.880s, instance15.520s, lookup15.920000s; scanned definition19.620s, instance19.880s, lookup21.265917s. Lookup reveals were moved within their existing phrases to provide1.011125s and1.50s reading windows, while preserving completed creation before lookup. These are explanatory edit anchors aligned to speech, not measurements of Java/Spring wall-clock behavior. The parent production verifies the actual compiled examples and encoded AAC mix separately.

## Outstanding essential voice requirement

**No auditory review was performed or claimed.** This runtime has no audio-ingestion/listening capability. Perceived younger-to-middle adult male age, smooth human explanation, every aspect of pronunciation and subtle synthesis artifacts cannot be perceptually accepted or rejected here. ASR, pitch, clipping and silence checks do not replace listening. Under the user's quality gate, **naturalness/listening acceptance remains incomplete**, despite actual licensed Kokoro narration and objective evidence being delivered.

Model/voice bundle hash checks passed. License evidence, locked dependencies, literal input/phoneme records and rebuild code are retained. Large model caches and virtual environments are excluded. No MOS surrogate, expected-transcript prompt or invented human approval was used.
