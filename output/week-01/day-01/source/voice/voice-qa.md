# Config overview and thanks narration QA

**Local Kokoro:80% am_puck /20% am_fenrir**, American-English male style blend, speed 1.02, CPU inference. Requested style is younger-to-middle adult, smooth explanatory delivery; perceived age and human naturalness remain unverified by listening.

## Actual file and synthesis

- Narration length **43.403417 s**,48,000Hz,mono,24-bit PCM.
- Seven whole-scene utterances, each asserted to fit exactly one inference batch. First-five-scene wording/timing unchanged. No mid-scene splices, pitch shifting, waveform speed change, external service or fallback TTS.
- Peak **-1.514414dBFS**, RMS **-21.123701dBFS**, **0 clipped samples**. Endpoint samples are zero. Quiet edit endpoints have 4 ms microfades.
- Signal above−60 dBFS starts at **0.015250s** and ends at **43.037479s**.
- pYIN voiced F0 10th/50th/90th percentiles: **86.84/111.96/171.08Hz**; variation **4.80 semitones** over2607 voiced frames. This supports pitch variation, not age/naturalness acceptance.

## Timing and continuity

Scene 6's source utterance ends at 39.962667 s, followed by an exact **2.0s completed-diagram hold to 41.962667 s**. Scene 7 thanks starts immediately after the hold, source utterance ends at 43.053417 s, and a350 ms final quiet tail completes the43.403417 s track. `thanks_end` means the full card/scene end, not just speech end.

The−45 dBFS/120 ms source silence scan shows the expected recap reading interval plus model decay at **39.318542–41.984750s** (2.666208s). This is deliberate quiet between recap speech and thanks, not a missing-speech dropout. Final source quiet is42.920146–43.403417 s (0.483271s), including decay andtail. Other inter-scene gaps/decays are≤0.845042 s; within-scene sentence pauses are≤0.326021 s. The complete99-word recognized transcript supports that no expected words disappeared. The final music bed/mix and encoded continuity are checked by the parent production.

## Independent pronunciation/intelligibility check

Whisper **base.en int8**, beam 5, no initial prompt: **99 expected normalized words**, **99 observed**, edit distance 0, raw normalized WER **0.0**. Config, Config's, Repo, Service, bean terminology, and Thanks for watching are recognized. Raw transcript and score remain unchanged in `asr.json`/`asr-summary.json`. G2P input evidence includes Config, possessive Config's, Repo, Service and thanks, in addition to distinct bean/being phonemes. This is objective pronunciation support, not perceptual listening.

No alignment-normalization exceptions were needed (`alignment-normalization.json=[]`). All 21 display cues match the script and are≤45 characters. Internal caption splits/overview anchors use approximate 20 ms-grid ASR times. Exact scene boundaries override ASR scene-onset errors; in particular the ASR placed the first Thanks word slightly early, and the caption uses actual synthesis scene start41.962667 s to keep the two-second hold intact. No transcript or audio was altered to force a score.

## Perceptual limit

The runtime cannot ingest audio for listening review. No auditory approval is claimed. The checks establish file integrity, complete recognized words, deliberate pauses, no clipping and varied pitch. They cannot certify the requested humanlike smoothness or age impression, or detect every subtle synthesis artifact. Strict voice naturalness acceptance remains **unverified**.

## Reproduction and evidence

`./setup.sh`; `.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20`; `.venv/bin/python qa.py --asr-model base.en`; `.venv/bin/python split_captions.py` (use spaces between option names and values as shown in the README).

Pinned model/voice hashes: `models.sha256`; package versions: `requirements-lock.txt`; official rights evidence: `licenses/`. Whisper is verification-only and contributes no audio to the final video. The model and voice hashes were rechecked successfully; raw logs and seven WAV segments are retained.
