# Asset rights and licensing record

Production: **What Is Spring IoC? — iSLDevs**. Rights review uses the actual retained assets and license evidence, rather than a stock-asset placeholder list.

| Asset | Actual source and use | Rights evidence |
| --- | --- | --- |
| Script and publishing copy | Original English text written for this production | `narration-script.md`, `youtube-metadata.md`, `facebook-metadata.md`; no quoted third-party script |
| Cover, diagrams and animation | Original Pillow drawing code, labels, colors and reference-motion sequences | `source/animation/render.py`; no stock footage, imported art or downloaded logo |
| Background music and sound effects | Original NumPy sine-based harmonic bed and short reference-transfer tones | `source/animation/audio_mix.py`; no sampled or licensed music recording |
| Male AI narration | Local Kokoro v1.0, 80% am_puck / 20% am_fenrir style embeddings | Apache-2.0 model distribution; official model card, male voice table, project license and release evidence in `source/voice/licenses/`; no separate noncommercial restriction identified for these used styles |
| Kokoro inference software | kokoro-onnx 0.6.1 | MIT license retained as `source/voice/licenses/kokoro-onnx-LICENSE.txt` |
| Open Sans font files | Installed Open Sans Bold, Regular and Semibold, copied into source assets | Apache-2.0, Google 2010–2011 copyright; notices in `source/assets/OpenSans-LICENSE.txt`, complete license in `source/assets/Apache-2.0.txt` |
| DejaVu Sans Mono | Installed font copied into source assets | Permissive Bitstream Vera license with DejaVu changes in public domain; full conditions/notices in `source/assets/DejaVu-LICENSE.txt` |
| Java/Spring example | Minimal Java example created for this lesson using standard API idioms | `source/java/IoCDemo.java`; actual build/run evidence in `source/evidence/java-*` |
| Spring and Micrometer dependencies | Pinned open-source runtime jars used for verification | Apache-2.0 notices and licenses retained in `source/java/licenses/` |
| Eclipse Java compiler | ECJ 3.40.0, used because the environment lacks javac | Eclipse Public License 2.0 evidence in `source/java/licenses/ecj-EPL-2.0.html` |
| Verification-only speech model | Whisper base.en through faster-whisper | Open-source verification dependency only; contributes no audio to the published video |

The retained third-party asset licenses permit commercial use subject to their terms. License texts and notices travel with the source package. Rendering/exporting used free/open-source Python, Pillow, NumPy, SciPy and FFmpeg/libx264/AAC tools. Virtual environments and model caches are excluded from the downloadable ZIP and are recreated using pinned setup scripts; actual downloaded Kokoro model/voice hashes are retained.

The iSLDevs name is rendered as text according to the user brief. No external iSLDevs logo file or third-party Spring/Java logo was imported. Java and Spring names and identifiers are used for factual technical explanation.

The narrator is AI-generated from licensed model styles, not a newly recorded human voice and not a requested imitation of a named person. The delivery target is a younger-to-middle adult male. Perceived age and human naturalness have not been accepted by listening because this environment cannot ingest audio; that quality limitation is separate from this asset-license record. No upload or publication has occurred.
