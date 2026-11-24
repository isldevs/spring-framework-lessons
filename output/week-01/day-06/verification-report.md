# Verification report — Multiple contexts

**Rendered and technically verified. Overall strict approval is INCOMPLETE because perceptual narration acceptance is unavailable.** No listening review, perceived-age acceptance or physical-phone playback test is claimed.

Approved curriculum: Multiple contexts; publication date **2026-11-21**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). The date is preserved despite production finishing later. No YouTube/Facebook upload, scheduling or publication was performed. Week/day/episode numbering is absent from the media and publishing copy.

## Actual final media

| Measurement | Actual result |
| --- | --- |
| Container duration | 38.116667 seconds |
| Picture | 1080×1920, H.264 High, 8-bit yuv420p, progressive |
| Frame rate/count | 60/1 constant FPS; 2287 frames and all timestamps checked |
| Audio | AAC-LC, stereo, 48000 Hz; encoded stream duration 38.112s |
| Color | Rec.709 matrix, transfer and primaries; limited/tv range; SDR |
| Integrated loudness | -15.88 LUFS |
| True peak / loudness range | -1.40 dBTP / 4.0 LU |
| Captions/scenes | 22 SRT cues, max34 characters; 7 scenes |
| Full-file decode | Exit0; empty FFmpeg error log |
| Black frames | No black intervals detected |

Master SHA-256: `af155cc6dd42523d81b3297e2c2d3caa45739e0fddb54643480273524dd5a302`.

Actual FFprobe JSON, commands, stdout/stderr and all-frame timestamp evidence are in `source/evidence/`. MP4 uses fast-start metadata. Rendering completed with exit0; `render.log` retains the2287-frame production trace.

## Genuine Java/Spring verification

Spring Framework6.2.11, OpenJDK21.0.13, ECJ3.40 targetingJava17; ten pinned dependency JARs with hashes/licenses. No Spring Boot, Maven or javac execution is claimed. Main compilation, test compilation, JUnit and app execution each exited0 with empty stderr. **4/4 actual JUnit tests passed**, zero failures/errors.

Tests verify independent A/B registries and missing cross-lookups; child-to-parent named fallback returns the exact parent singleton while containsLocalBean and local definitions remain separate; no parent-to-child lookup by default; and child same-name shadowing. Child is linked before refresh and closed before its parent. Actual tested-source hashes, raw command evidence, JUnit XML and application output are retained. The media validator checks that evidence and does not pretend to rerun Java.

Actual application stdout:

```text
A alpha: alpha
B beta: beta
A beta: missing
A beta exception: NoSuchBeanDefinitionException
B alpha: missing
B alpha exception: NoSuchBeanDefinitionException
child shared: shared
child shared same: true
child owns shared: false
child local: local
parent local: missing
parent local exception: NoSuchBeanDefinitionException
parent active after child close: true
```

Five official Spring6.2.11 API pages were fetched with HTTP200: BeanFactory, HierarchicalBeanFactory, ListableBeanFactory, ConfigurableApplicationContext and AnnotationConfigApplicationContext. HTML hashes and exact claim excerpts are retained in `source/evidence/java-doc-*`; the two publishing references were independently fetched and hashed. Scope is **named lookup**: local-name precedence, parent fallback and absent reverse visibility are not generalized to every type enumeration API.

## Opening, diagrams and mobile readability

The first frame shows two independent registries, the same alpha lookup and different outcomes. No static cover hold, black frame, greeting or fade-in precedes the hook. The separate1080×1920 cover is not inserted as an opening delay. Source speech begins at0.014979s; the whole spoken hook ends at1.705292s. The first2s encoded audio RMS is-15.83dBFS. Core visual motion starts at1/60s; 52 distinct opening core frames were observed. Five actual encoded opening snapshots match their source states, minimumSSIM0.998719.

Renderer preflight sampled217states,137unique text bounds, zero safe-area violations. Final validation sampled253 source states plus36 actual decoded states with no margin violations inside X90..990/Y250..1520. These are sampled visual/bounds checks, not a claim of manual inspection of every frame.

Root inspected the actual decoded seven-scene contact sheet, all six transition pairs, five opening snapshots, parent-return/reverse-missing anchors and the actual final frame. Headings, bean names, key lookup code and captions remain inside safe margins. Smaller configuration/type labels are supporting detail. Named requests stay tied to the correct context; parent/child remain fresh separate registries; the parent shared instance stays in the parent while only its reference returns. The failed reverse lookup remains in the parent. No caption/diagram collision or clipped label was observed in those reviewed stills. This is still-image review, not a physical-phone or real-time listening review.

Edit anchors, in seconds: registration2.66; independent lookup8.898042/missing11.40; parent link18.06 before child refresh19.06; child local check23.16; parent fallback26.34/reference return26.54; reverse request27.34/missing28.62; complete overview34.63. They illustrate causality and are not Spring wall-clock measurements.

## Recap and ending

The completed overview reading hold is **34.771750–36.771750s**, exactly2s, before the separate spoken Thanks. All120source core frames are pixel-identical. All120encoded hold frames were compared, minimumSSIM0.998061. Final picture frame2286 matches the expected Thanks state withSSIM0.998743. The closing text is “Thanks for watching.”

## Kokoro voice, synchronization and continuity

Licensed local Kokoro v1.0 male80%am_puck/20%am_fenrir blend, normal1.02 inference speed, seven coherent scene utterances; no pitch shift, waveform stretching or word splicing. Source WAV is38.112500s,48kHz mono PCM24. Its SHA-256 is `f6aa1ffad01550e40ea0c7c01e68572ad437ddf214460d96ce9bb3aa7525953b`. Source peak-1.514414dBFS,0clipped samples, zero endpoints. Median voicedF0115.24Hz/variation4.65semitones are signal metrics, not perceived-age/naturalness judgments.

Context-label A was corrected to/eɪ/ through a recorded targeted phoneme override within a coherently regenerated scene. Final unprompted faster-whisper small.en int8 recognizes91expected/91observed words with2substitutions, rawWER**2.1978%**, not zero: “registries stay”→“registry stays.” Raw transcript/score are unchanged. Two caption-only token mappings use the observed spans with explicit provenance; caption text follows the actual known synthesis input and correct recorded phonemes. No ASR listening acceptance is implied. Final ASR metadata matches the current narration WAV hash.

SRT captions follow final scene/sample boundaries and approximate20ms ASR word spans; all display words match the final91-word script. Ordinary joins are0.08s; the separate recap hold is intentional. Longest pre-hold source quiet interval is0.548875s. Encoded silence scan only finds the intended final quiet tail beginning37.902729s. Original quiet NumPy harmonic bed is ducked below speech, with six effects cued to the same narrated reveals; two-pass EBU normalization and full decode/continuity evidence are retained. No third-party sampled music is used.

**Outstanding essential requirement:** no supported auditory listening capability is available here. Smooth human delivery, pronunciation, perceived young-to-middle adult age and absence of subtle synthesis artifacts have not received perceptual acceptance. Automated transcript, G2P, pitch, pause and clipping checks cannot replace it. The actual narrated video is delivered, and strict completion remains incomplete for this requirement.

## Phone delivery and platform copies

Owner-private player: https://isldevs-multiple-contexts-player.sivlayyi-bs.chatgpt.site . Native Sites reports successful deployment. It serves the unchanged MP4 with native controls/playsinline and same-origin downloads for MP4, cover and SRT. Source commit, deployment ID, archive/hash/wiring/syntax checks and access scope are recorded in `source/mobile-preview/deployment.json`. The owner may need to sign in with their ChatGPT account. Browser and physical-phone playback were not tested because the managed browser tool was unavailable.

Both platform MP4 copies were independently probed and fully decoded, with empty error logs; each is byte-identical to the master. Exact covers/SRT, platform manifests and upload ZIP CRC checks passed. Final `checksums.sha256`, three archive checksums and the production ZIP are generated only after this report and source freeze; `day-06-delivery-audit.json` records the actual manifest/member/hash/CRC results. No finalization success is inferred from this report alone.

The separate asset-rights and originality records describe actual software/font/model licenses and original graphics/audio/code; no global novelty/plagiarism claim is made. Reproducible Java, animation, voice, audio and phone-player sources are preserved. Speech models, environments, caches and bytecode are excluded from delivery.
