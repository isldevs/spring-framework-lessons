# Asset rights — How Spring Dependency Injection Works

This record identifies the production inputs and retained license evidence. It is an asset-provenance record, not a claim of final audiovisual acceptance.

| Input | Source and use | Permission/evidence |
| --- | --- | --- |
| English script and platform copy | Written for this iSLDevs explanation of configured scanning, constructor resolution and reference injection | Retained narration script, publishing text and generation source; no third-party article or video transcript supplied as the script |
| Cover, diagrams, recap and Thanks card | Procedural Pillow graphics and typography using retained drawing code | `source/animation/render.py`; assets are fonts rather than stock photographs, illustrations or footage |
| Music and reference-transfer sounds | Original NumPy-generated harmonic tones, envelopes and event timing in the production audio source | `source/animation/audio_mix.py`; no sampled song or stock sound recording is part of the production design |
| Male AI narration | Locally generated Kokoro v1.0 voice style, 80% `am_puck` / 20% `am_fenrir` | Apache-2.0 model distribution; official model card, male voice table, license and release record retained under `source/voice/licenses/` |
| Kokoro inference software | kokoro-onnx | MIT license retained as `source/voice/licenses/kokoro-onnx-LICENSE.txt` |
| Open Sans fonts | Unmodified Bold, Regular and Semibold font files | Apache-2.0; notices and complete license in `source/assets/OpenSans-LICENSE.txt` and `Apache-2.0.txt` |
| DejaVu Sans Mono | Unmodified code font | Permissive Bitstream Vera terms, with DejaVu changes in the public domain; `source/assets/DejaVu-LICENSE.txt` |
| Spring verification dependencies | Pinned Spring Framework and Micrometer jars | Apache-2.0 licenses/notices under `source/java/licenses/` |
| Java compiler | Eclipse ECJ used with the installed Java runtime | Eclipse Public License 2.0 evidence under `source/java/licenses/` |

The retained third-party licenses permit commercial use subject to their terms. Both used Kokoro styles are identified as American English male voices in the official table; no separate noncommercial restriction is identified in the used model distribution. Model and voice downloads are pinned by `source/voice/models.sha256`. Font files and required notices accompany the source package.

The iSLDevs name is rendered as text according to the user brief. No external iSLDevs, Java or Spring logo image is required. Java and Spring identifiers describe the technical example. Production uses free/open-source software; no paid asset, proprietary font, sampled music recording or stock clip is listed among the inputs.

Narration is synthesized from licensed pretrained styles, not a newly recorded human performance or a requested imitation of a named person. Perceived age and smooth human naturalness remain unverified by listening in this runtime. See `verification-report.md` for actual rendering, encoding and remaining voice-review status. No YouTube or Facebook upload or publication is claimed here.
