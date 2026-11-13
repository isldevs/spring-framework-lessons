# Recap narration verification

Current voice is **80% local Kokoro am_puck + 20% am_fenrir**, American English male style embeddings, speed 1.02, CPU inference through kokoro-onnx 0.6.1. Delivery target remains a younger-to-middle adult explanatory male voice. Perceived age and smooth human naturalness are not established by these measurements.

## Actual generation

The first five scene texts and edit timings are unchanged. Scene six is a whole-flow recap: define the beans, Spring creates and wires them, the application requests the ready service, and the managed-bean qualification. All six complete scenes fit exactly one model inference batch; scene six has 218 phonemes. There are no mid-scene speech edits. Source script and full G2P phoneme checks are retained in `generate.py` and `pronunciation-g2p.json`.

Inter-scene added gaps are 200–260 ms. The final scene speech edit ends at **42.367792 s**, followed by an exact **2.0-second programmed diagram hold** to **44.367792 s**. Model ending decay adds quiet time beyond those explicit gaps. Quiet edit endpoints use 4 ms microfades. There is no pitch shifting, time stretching, substitute TTS or artificial initial silence.

## Objective measurements

- Source narration length **44.367792 s**, 48 kHz mono PCM24.
- First signal above −60 dBFS at **0.015250 s**. Last above-threshold signal at **42.352583 s**.
- Peak **-1.514415 dBFS**, RMS **-20.874903 dBFS**; **0 clipped samples**. Both endpoint samples are exactly zero.
- pYIN voiced pitch 10th/50th/90th percentiles: **86.34/112.61/168.73 Hz**; **4.85 semitones** standard deviation across **2700** voiced frames. This supports varied pitch, not age or naturalness acceptance.
- Source FFmpeg −45 dBFS silence scan, 120 ms minimum: longest internal quiet interval is **0.846646 s** at the verification-to-recap transition; source final quiet interval is **2.688479 s**, including native decay plus the deliberate two-second hold. Longest within-scene sentence pause is approximately 0.325 s. Full log is `silence-scan.txt`.

## Independent recognition and caption alignment

Whisper **base.en int8**, beam size 5, no initial prompt: **102 expected words**, **103 ASR tokens**, raw edit distance **2**, raw normalized WER **1.96%**. The sole lexical discrepancy is “inversion” segmented into “in version.” It is retained in the actual raw transcript; it is not missing speech and no 0-WER claim is made. The source G2P uses the intended inversion phonemes. Bean `/bˈiːn/` and being `/bˈiːɪŋ/` remain distinct in the phoneme evidence.

For caption alignment only, those two adjacent ASR tokens are merged into inversion with their combined start/end interval. This explicit normalization is recorded in `alignment-normalization.json`; all remaining aligned words must match the intended narration exactly or the script stops. There are **23** short display cues, at most **45** characters, using approximate ASR word timestamps on a 20 ms grid. Spoken get bean is displayed as `getBean`.

`../timing.json` records exact scene edit boundaries, the original script, relative and absolute recap anchors, and final hold timing. ASR-based anchors include Define 30.62 s, create 32.12 s, wire 33.16 s, application request 35.14 s, ready 36.56 s, takeaway 37.68 s, qualifier 38.58 s, and complete graph by 39.98 s. The final two-second hold starts at 42.367792 s.

## Perceptual limitation

This runtime cannot ingest audio for listening review. No auditory review was performed or claimed. Automated transcript, peak, pause and pitch checks cannot certify the requested age impression, smooth human naturalness or absence of every synthesis artifact. Strict perceptual voice acceptance remains **unverified**.

## Reproduce

`./setup.sh`; `.venv/bin/python generate.py --speed 1.02 --voice am_puck80_fenrir20`; `.venv/bin/python qa.py --asr-model base.en`; `.venv/bin/python split_captions.py`.

The local model and voice bundle are pinned by `models.sha256`; inference and verification dependencies by `requirements-lock.txt`. Model/voice/software license evidence remains in `licenses/`. Verification-only Whisper contributes no speech audio.
