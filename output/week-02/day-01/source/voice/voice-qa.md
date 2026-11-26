# Actual narration QA

Local Kokoro v1.0, male80%am_puck/20%am_fenrir, normal1.02 across7coherentbatches; no pitch shift, waveform stretch or isolated-word splice. Initial78-word34.081542s candidate was superseded by adding “Spring selects it automatically.” to scene2 and regenerating that whole utterance; final82whitespacewords produce36.261917s. Candidate logs are clearly marked trials.

Final48kHz monoPCM24 SHA256:55029410b326510b359fccfb0dbfd556511b35ca08feddda25e7b256f45d4e48. Actual signal onset0.015021s,end35.996604s;peak−1.514415dBFS,RMS−19.825931dBFS,0clipped,zero endpoints. VoicedF0median113.26Hz/std4.63semitones cannot establish human naturalness or age. Longest pre-hold−45dBFS quiet interval0.519979s,8.167438–8.687417. Ordinary scene edit joins0.08s; deliberate complete recap hold32.921167–34.921167 precedes spoken Thanks.

Hook utterance1.755125s; observed final hook word ends1.52s. Whole hook is a single cue0–1.755125 for the exact sourcecover opening. Final20cues,max41characters,3–6whitespacewords each. Renderer uses the separately approved52pxInterBold rounded black82%panels. Primary raw unprompted small.en int8 has83expected/86observedtokens,6edits,7.2289%WER; only compound/camelCase spelling differs: Autowired→auto-wired twice,PaymentGateway→payment gateway. Three caption-only span merges are explicit; no raw score/transcript/timing is altered or promoted to zero-error. No phoneme override was needed; recorded G2P is not a listening review. CurrentASRmetadata is hashed to this WAV.

Model/stylebank hashes were actually checked in model-check.log. Licenses, lockfiles, inputs, raw/derived alignment evidence, generator and clean scene recordings are retained. Temporary model/environment symlinks are removed without deleting shared cached assets.

**Essential auditory acceptance remains INCOMPLETE.** No supported listening/audio-ingestion tool exists in this chat; no human-style smoothness, pronunciation, rhythm, joins or perceived-age approval is claimed. Automated recognition, G2P, signal/pitch/pause tests cannot substitute for that review. No other TTS fallback is used. Mixed AAC/continuity is measured separately by the final media validator.
