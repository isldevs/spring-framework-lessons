# Narration QA — constructor injection in Spring Boot

## Actual source measurements

- Local Kokoro 80%am_puck/20%am_fenrir, model inference speed0.90, seven coherent single-batch utterances. No substitute TTS, pitch shifting or waveform time stretching.
- **35.819167s**,48 kHz mono PCM24; frame-rounded MP4 **35.833333s**.
- Signal above−60dBFS begins **0.015813s** and ends **35.419271s**. No artificial initial silence.
- Peak **-1.514415dBFS**, RMS **-22.351673dBFS**, **0clipped samples**. Both waveform endpoints are zero; quiet joins use4ms microfades.
- Voiced pYIN F0 10th/50th/90th percentiles **91.47/117.26/164.87Hz**, variation **4.04semitones** over2009voiced frames. These support varied pitch, not humanlike naturalness or perceived age.

## Independent recognition and preserved raw omission

Unprompted Whisper base.en int8, beam5, no initial prompt, full-stream decoding recognizes74normalized main-lesson words exactly and omits only the three-word Thanks for watching after the recap reading hold. Raw measurements: **77expected/74recognized**, edit distance **3**, normalized WER **0.038961 (3.8961%)**. Original asr.json/asr-summary.json are preserved; do not claim full-stream zero WER.

A separate unprompted transcription of the actual final crop **34.283125–35.819167s** recognizes **Thanks for watching** exactly,3/3words. supplemental-asr.json records recognized words, confidence values and absolute times. asr-alignment.json combines untouched first-six-scene ASR with these independently observed final-phrase times; no expected words were silently inserted and raw WER remains unchanged.

Combined recognition covers all77expected normalized words. Captions retain ordinary spaced 'payment gateway'/'order service' wording. There are **18display cues**, maximum **40characters**. Word boundaries use approximate20ms-grid ASR times; scene/hold edits are sample-derived. alignment-normalization.json records no text changes and explains the derived constructor-ready and recap-complete animation anchors. Full G2P inputs are in pronunciation-g2p.json.

## Rhythm and synchronization

The−45dBFS/120ms source silence scan finds the longest pre-hold quiet interval **0.632437s** at7.903062–8.535500s, between explanation and Boot discovery. The recap-to-Thanks quiet span **31.759208–34.326479s** lasts2.567271s, including native decay and the exact2s reading hold. The final quiet tail35.326812–35.819167s lasts0.492354s. The complete transcript is present across the two independent decoding passes; no unexpected missing speech was observed. silence-scan.txt and silence-summary.json preserve raw thresholds and intervals.

Recap hold: **32.283125–34.283125s**, before the Thanks card. Constructor passage begins13.780s; constructor word15.260s; documented graph-ready completion15.610s precedes business-order placement17.180s. These are animation/speech anchors, not Java wall-clock execution timings. Parent production separately verifies the actual Spring Boot behavior and encoded mix.

## Outstanding essential voice requirement

No auditory review was performed or claimed. This runtime cannot ingest audio for listening, so perceived younger-to-middle adult age, smooth human explanation, subtle synthesis artifacts and every aspect of pronunciation cannot be perceptually accepted or rejected here. ASR, pitch, silence and clipping metrics are not substitutes for listening. Under the user's completion criterion, **voice naturalness acceptance remains incomplete**, despite actual licensed Kokoro audio and objective evidence being delivered.

No MOS surrogate or transcript prompt was used to manufacture a listening result. Final AAC loudness and continuity are checked separately; these figures describe the clean source WAV. Model/voice bundle hashes were rechecked successfully; license evidence and reproduction inputs remain under this source folder.
