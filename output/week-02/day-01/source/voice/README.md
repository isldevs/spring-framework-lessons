# Local Kokoro narration — Constructor injection

Use `bash setup.sh`, then the generated local `.venv/bin/python generate.py --speed 1.02 --hook-speed 1.02 --voice am_puck80_fenrir20`, `qa.py --asr-model small.en`, and `split_captions.py`. Run these commands from this directory, or use the lesson's source/rebuild.sh. The literal approved inputs are ../script-input.json. The model/style bank is downloaded by setup with retained hashes/licenses; binary models/environments are excluded from delivery.

Seven coherent utterances use a licensed male80%am_puck/20%am_fenrir blend. The second scene was regenerated as a whole to add the useful single-constructor selection explanation. No slowing, pitch shifting, waveform stretching or word splicing. No phoneme override was required.

Final clean narration36.261917s/48kHz monoPCM24; all speech at normal1.02. Hook is exactly No Autowired? This still works. The first caption deliberately starts0 and ends at the exact1.755125s utterance endpoint so it is part of cover/sourceframe0. The entire cover headline is different, so it does not replace this caption.

Primary unprompted small.en int8 recognizes83normalizedreference/86observedwords with6edits,WER7.2289%. Literal input has82whitespacewords; Spring-managed splits in recognition normalization. Three caption-only span merges cover two Autowired→auto/wired phrases and PaymentGateway→payment/gateway. Raw transcript, word times and score remain unchanged. Captions use known synthesis text and observed approximate20ms spans plus sample-derived scene/edge edits; no even-time word interpolation or fictitious subword times. See alignment-normalization.json and asr-alignment.json.

Final20cues are3–6whitespacewords,max41characters; renderer wraps at52pxInterBold to at most2lines,max840px padded width. Models, licenses, hashes, dependency lock, phonemes, sceneWAVs and actual metrics preserve reproduction. An actual listening review was unavailable: naturalness, pronunciation and perceived age remain UNVERIFIED, irrespective of ASR/G2P/signal/pitch results.
