# Narration QA — ApplicationContext

## Actual source and opening

- Local Kokoro v1.0,80% am_puck /20% am_fenrir, one coherent inference batch per scene. Hook inference speed1.00; scenes2–7 speed0.90. No fallback TTS, pitch shifting or waveform time stretching.
- Final source duration **35.812000s**,48kHz mono PCM24. Picture rounds up to **35.816667s / 2149frames** at60FPS.
- Spoken hook: **What’s inside application context?** Public type spelling is ApplicationContext. The source utterance spans0–1.963s; raw unprompted ASR places its last context word end at **1.400s**. Signal above−60dBFS begins **0.015125s**, so there is no delayed narration or title-card silence.
- Source peak **-1.514414dBFS**, RMS **-20.529496dBFS**, **0clipped samples**. Both endpoints are zero; quiet joins use4ms microfades.
- Voiced pYIN F0 10th/50th/90th percentiles **89.90/114.58/168.73Hz**, variation **4.21semitones** over2031voiced frames. These metrics do not prove perceived age or human naturalness.

## Independent recognition and alignment

Actual unprompted faster-whisper base.en int8, beam5, no initial prompt recognizes **67/67normalized words**, edit distance **0**, normalized WER **0.000000** across the full stream, including Thanks for watching. This zero-WER result describes the actual final narration, not a manufactured expectation prompt. Raw text, word confidence and approximate timestamps remain in asr.json/asr-summary.json. supplemental-asr.json records that no separate phrase transcription was needed.

There are **18caption cues**, maximum **36characters**. Public ApplicationContext/getBean spellings map explicitly to spoken application context/get bean; no spoken words are changed or inserted. A conditional cleanup/clean up orthographic alignment rule is retained for reproducibility but was not needed in the final exact transcript. A rejected “What’s in…” candidate remains separately labelled under candidates/; its poorer raw score is not the final score.

ASR recognition accuracy does not establish exact word timing: the raw Thanks word begins33.32s even though that scene’s known sample edit is34.275958s. Caption first/last boundaries therefore use exact synthesized utterance edits, preserving the raw ASR evidence; intermediate word starts are clamped within their own utterance. This is an alignment correction based on actual edit points, not a claim that audio existed during the silent reading hold. G2P inputs and every scene’s phonemes remain in pronunciation-g2p.json.

## Rhythm and sync anchors

The−45dBFS/120ms source scan finds the longest pre-hold quiet interval **0.662604s** at14.330396–14.993000s, between creation and lookup. The recap-to-Thanks quiet span31.819250–34.319292s includes native decay plus the exact reading hold **32.275958–34.275958s**. Thanks begins at **34.275958s**, followed by the final quiet tail through35.812000s. Raw scan logs and thresholds are retained.

Animation anchors use observed words and documented illustrative substeps: refresh9.460s; definitions11.460s; creation12.400s; derived Repo12.480s then Service13.080s; lookup request15.260s and return15.740s; custom event21.560s; close22.480s; cleanup23.480s. The overview completes28.680s before its two-second reading hold. These are explanatory animation/speech times, not measurements of Spring’s runtime execution speed. The parent separately verifies the actual Java behavior and final encoded mix.

## Outstanding essential voice requirement

**No auditory review was performed or claimed.** This runtime cannot ingest audio for listening. Perceived younger-to-middle adult male age, smooth human explanation, subtle robotic artifacts and every pronunciation detail cannot be perceptually accepted or rejected here. Automated transcript, F0, clipping, silence and loudness checks are not substitutes. Under the user’s final quality gate, **voice naturalness acceptance remains incomplete** despite the actual licensed Kokoro audio and objective evidence.

Model and voice bundle hashes were rechecked successfully. Final AAC loudness/audio continuity are verified separately by the parent; the measurements above describe the clean WAV. No YouTube/Facebook upload or publication is performed by these voice tools.
