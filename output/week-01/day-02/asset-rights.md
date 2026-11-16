# Asset rights — ApplicationContext

This record identifies production inputs and retained license evidence. Technical file verification and perceptual voice acceptance are recorded separately.

| Input | Source and role | Rights evidence |
| --- | --- | --- |
| English narration and publishing copy | Original lesson text about bean definitions, managed instances, getBean lookup, event dispatch and cleanup | Narration script and publishing files retained; no third-party transcript copied as the script |
| Cover, animated hook, mechanism graphics, recap and Thanks card | Procedural Pillow text, recipe documents, reference/object graphics and shapes in the continuing iSLDevs style | `source/animation/render.py`; no stock photography, footage or imported third-party illustration |
| Background bed and effects | Own-production NumPy harmonic synthesis and timed mechanism cues | `source/animation/audio_mix.py`; no sampled song or stock recording |
| Male AI narration | Local Kokoro v1.0, am_puck/am_fenrir style blend | Apache-2.0 model distribution; model card, voice table, release evidence and license under `source/voice/licenses/` |
| TTS inference code | kokoro-onnx | MIT license retained under `source/voice/licenses/` |
| Open Sans fonts | Unmodified local Bold, Regular and Semibold font assets | Apache-2.0 notices and full license under `source/assets/` |
| DejaVu Sans Mono | Unmodified local code font | Bitstream Vera permission terms and public-domain DejaVu changes; `source/assets/DejaVu-LICENSE.txt` |
| Spring Framework and Micrometer jars | Pinned actual ApplicationContext verification runtime | Apache-2.0 licenses/notices under `source/java/licenses/` |
| Java compiler | Eclipse ECJ with the installed Java runtime | EPL-2.0 evidence under `source/java/licenses/` |
| JUnit verification tools | JUnit Platform Console Standalone 1.12.2 and bundled helper libraries | Actual license/notice files under `source/java/licenses/` |

The retained third-party asset licenses permit commercial use subject to their terms. Both Kokoro styles used are listed as male English voices within the licensed model distribution. Model and voice downloads are checksum-pinned by `source/voice/models.sha256`; Java dependencies have pinned download provenance and SHA-256 records. Downloaded speech-model caches and virtual environments are excluded from Git and delivery ZIPs.

Production uses free/open-source Python, Pillow, NumPy, SciPy and FFmpeg/libx264/AAC tools. The project's own drawing/audio helpers and font assets may be reused across lessons; that reuse is not represented as fresh worldwide invention. The iSLDevs brand is rendered as text according to the user brief, without an imported logo asset. Spring and Java names identify the technical example.

Narration is synthesized from licensed pretrained styles rather than recorded from a human or requested as an imitation of a named person. Intended adult male age and smooth human naturalness require actual listening. No auditory approval is claimed because this runtime cannot ingest the audio for that review. No automatic YouTube/Facebook upload, scheduling or publication is performed.
