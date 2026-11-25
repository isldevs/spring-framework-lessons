# Actual voice QA — Context smoke test

Local Kokoro v1.0;80%am_puck/20%am_fenrir male English blend;1.02 in all seven coherent scenes. No pitch shift, time stretching or individual-word splice. Root-approved concise scene3/6 edits shorten the original89-word41.940083s candidate to78words and **36.985542s**, without slowing narration.

Actual source:48kHz mono PCM24; SHA256`cbbedc48165a835978f87a82d162d72182ab52684a492f75fc9accae0f3080ff`. Signal above−60dBFS starts0.015104s and ends36.713563s. Peak-1.514415dBFS; RMS-21.825462dBFS;0clipped samples; both endpoints zero. VoicedF0median113.26Hz, standard deviation4.62semitones. These do not establish age or naturalness.

Primary raw unprompted small.en int8 recognition has78expected/78observed words,6edits,WER7.6923%. Its current-WAV hash is recorded. Exact differences: two bean→being substitutions, they're→they are expansion, look up→lookup compound spacing. The raw transcript/score are unmodified. Four documented caption-only mappings use observed spans: two bean labels; contraction span merge; shared compound span for look/up with no fake subword timing. G2P explicitly contains/bˈiːn/ and/dʒeɪ juːnɪt/; that does not certify what a human listener hears.

The separate unprompted base.en crosscheck has3edits/78words,WER3.8462%: two bean→beam substitutions and they're→there. Both recognizers leave the technical noun uncertain; neither is a listening approval. No zero-error result is claimed.

Actual final SRT has20cues,max34characters. Hook utterance ends1.837792s; observed final hook word ends1.68s. Whole final utterance/sample boundaries constrain ASR drift; intermediate timestamps are approximate20ms recognition estimates. The zero-duration observed Load token is retained. Closing diagram Load32.26/lookup32.42/assert32.64/complete33.17 uses an explicitly derived160ms illustrative reveal offset. The complete core reading hold is33.644792–35.644792s, exactly2s before Thanks. No runtime-performance claim.

Source−45dBFS/120ms silence scan retained. Longest quiet interval before recap hold:0.593583s (9.517125–10.110708s). Actual silent recap/closing intervals and final tail are in silence-summary.json. Final mixed AAC loudness/continuity and encoded platform copies are checked by the main production pipeline.

**Outstanding essential requirement: perceptual auditory acceptance is INCOMPLETE.** No actual listening/naturalness/pronunciation/perceived-age review is claimed because no supported listening capability exists here. Model/style-bank hashes were actually checked in model-check.log. Locks, license evidence, literal inputs, coherent scene recordings, code and recognition/provenance evidence preserve reproducibility. Temporary model symlink, virtual environment and bytecode are excluded/removed before handoff.
