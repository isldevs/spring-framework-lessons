# Local Kokoro narration — Bean registration

The delivered source WAV is actual local Kokoro inference using 80% `am_puck` / 20% `am_fenrir` male English styles. The model distribution is Apache-2.0 and kokoro-onnx inference code is MIT; retained evidence is under `licenses/`. `models.sha256` pins the model and voice bundle, and `model-check.log` records their successful current hash checks. Models, environments and caches are not redistributed.

Final narration is **38.387208 seconds**, 48kHz mono PCM24; its video picture rounds up to **38.400000 seconds / 2304 frames at60FPS**. The hook is **“Why isn't this a Spring bean?”**, shortened for pacing while the opening image explicitly shows the plain Java class and missing Spring registration. The source hook utterance is1.486333s and raw ASR's final hook word ends1.040s.

Literal speech inputs are in `../script-input.json`. Each scene is synthesized as one coherent inference batch, without pitch shifting or waveform time stretching. Hook inference is1.00; the remaining scenes use0.80. This body pace was selected after the initial0.95 candidate was below the requested35–40s duration. It is a lesson-specific model setting, not an auditory-approved universal voice profile.

The original fourth phrase produced a class-as/class's recognition ambiguity in both full-stream and independent crop recognition. With parent authorization it was rewritten as **“Or add the component annotation, then scan the package containing your class.”** That whole coherent scene was regenerated; the other six saved scene utterances were reused. Rejected recognition evidence is retained under `trials/`, separately from the final raw transcript.

## Reproduce from the lesson directory

```sh
bash source/voice/setup.sh
source/voice/.venv/bin/python source/voice/generate.py --speed 0.80 --hook-speed 1.00 --voice am_puck80_fenrir20
source/voice/.venv/bin/python source/voice/qa.py --asr-model base.en
source/voice/.venv/bin/python source/voice/split_captions.py
```

A full rebuild creates all seven scene segments from the final inputs. The optional `--regenerate-scene 4` flag reuses already generated segments for other scenes and regenerates only that complete phrase; it requires those saved clips to exist. It does not splice within a spoken utterance. `generate.py` preserves natural interior pauses, trims only outside quiet padding with a15ms consonant guard, resamples24→48kHz and applies4ms quiet-end microfades.

`qa.py` performs unprompted faster-whisper base.en int8 recognition, beam5, without an initial prompt. It preserves raw `asr.json` and strict `asr-summary.json`, then computes clipping, endpoints, onset and pYIN pitch measurements. The final raw result is **72 expected words /73 recognized words, edit distance2, WER0.027778 (2.7778%)**. The only mismatch is the technical compound **classpath**, recognized as **class path**. Alignment explicitly canonicalizes that compound spelling; it does not rewrite the raw recognition score or fabricate missing words. No supplementary final-phrase transcription was needed. Public captions format spoken bean/component as `@Bean`/`@Component`, using punctuation-only comparison.

`split_captions.py` writes18display cues, maximum35characters, with exact sample-derived utterance boundaries and intermediate ASR word anchors. First/last caption boundaries use the known synthesis edits if short-outro ASR timestamps drift. Derived factory/scanning/lookup/recap substeps are documented in `alignment-normalization.json`; these are explanatory video timings, not measurements of Spring execution speed.

The complete recap reading hold is **34.679125–36.679125s**, exactly2s. The separate Thanks scene then runs **36.679125–38.387208s**, including its audio tail. The hook begins immediately; no static cover hold is inserted.

## Essential acceptance limit

**No auditory listening review was performed or claimed.** Current tools do not ingest this audio for listening. Humanlike smoothness, final pronunciation, subtle synthesis artifacts and perceived younger-to-middle adult age remain incomplete acceptance criteria. ASR, pitch and silence measurements support technical quality but cannot substitute for that review. No fallback TTS was used. See `voice-qa.md` and the lesson verification report for the actual measured evidence and limits.
