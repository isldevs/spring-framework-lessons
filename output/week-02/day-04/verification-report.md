# Verification — Circular dependencies

**Production INCOMPLETE for perceptual listening acceptance.** Actual narrated MP4 rendered and technically verified. No supported auditory-review tool was available; smoothness, terminology pronunciation, rhythm and perceived age remain unverified. Browser/physical-phone playback is untested. No social upload, scheduling, thumbnail selection or live-player deployment occurred.

Approved topic **Circular dependencies**, publication **2026-11-26**, proposed19:00Asia/Phnom_Penh(12:00UTC). Date/sequence unchanged despite later production; no public week/day/episode numbering.

## Actual encoded export

- Duration 37.700000s; native1080×1920/60FPS/2262frames; H.264/AAC stereo48kHz,8-bit yuv420p,Rec.709SDR. Fast-start moov-before-mdat verified.
- Full decode clean,empty error log,0black intervals. All2262 frame timestamps checked at60FPS.
- Final measured-15.90LUFS/-1.18dBTP. Objective audio/silence logs retained; signal checks do not establish listening acceptance.
- Master SHA256 `355c777fbd5b923956dd5c6cbb0176d5dcdf07e6fa26c43c0316a61fdc732555`.

## Genuine Java verification

**2/2 actual JUnit tests passed**,zero failures/skips. Spring/spring-test6.2.11,JUnit5.12.2/platform1.12.2,ECJ3.40target17,actualJDK21.0.13. Eleven pinned JARs with hashes/licenses retained. Main/test compile and JUnit exit0; expected negative refresh warning preserved in stderr. Current two Java source hashes match those executed.

Configs.Cycle registers Broken.ServiceA(ServiceB) and Broken.ServiceB(ServiceA) through @Import. The test explicitly enables circular references, asserts UnsatisfiedDependencyException at refresh and deepest BeanCurrentlyInCreationException, and checks inactive context. Full actual stack trace retained. Constructors cannot receive completed arguments, so this is a constructor cycle; the pictures are pending creation requests, not completed instances waiting at runtime.

Configs.Acyclic registers independent Fixed.ServiceA/B and Orchestrator(A,B). Test verifies active context, zero-parameter A/B constructors, exact managed references injected into Orchestrator and execute() result A then B. It does not claim comprehensive business correctness or Boot-specific behavior. No standalone main execution claimed.

Actual proof lines:

```text
acyclic context: started
managed references: same
orchestration result: A then B
constructor cycle: startup failed
outer exception: UnsatisfiedDependencyException
nested cause: BeanCurrentlyInCreationException
```

Official pinned Spring6.2 dependency-injection documentation returnedHTTP200; full page/hash and exact constructor-cycle excerpt retained. It explicitly discusses A→B→A constructor injection and BeanCurrentlyInCreationException. Other circular references can behave differently, including early references in some setter/field cases/configurations. Neither @Lazy nor enabling circular references is offered as a universal production fix. This film teaches removal of the graph cycle via orchestration.

## Cover, captions and motion

Four-line white Inter900/opsz32,96px headline: Why Spring / Fails With / Circular / Dependencies. Only Circular has#0866FF highlight,radius20,padding18/8. InterOFL/fontprovenance retained. Complete cover composition is visible in sourceframe0 and equals cover.png exactly, including the separate full-hook caption.61headline samples0–1s stable; creation-request carrier moves from1/60s. From1–2s the actual A/B creation diagram moves into explanation as the headline retires; no fade to black.

Actual encoded0/.5/1/1.25/1.5/1.75/2s frames compared with source; frame0meanRGBerror1.357201. Lossy decoded pixel identity is not claimed. first-frame.png is extracted from the actual MP4. Square/portrait/feed crop previews retained; manual platform crop/frame choice required.

Captions Inter700/52px white, measured Pillowtextbbox,RGBA blackalpha209≈82%,rounded12,padding26/14,dynamicmax840,center540/1380,max2lines.17coherent3–7word cues, final script words. Dedicated caption region prevents technical overlap. Source preflight250states,zero safe-bound violations withinX90..990/Y250..1520. Final ASR observed word windows and sample-derived scene edges supply synchronization, not evenly divided timing. Raw ASR record remains unchanged; no display mappings needed on this final run.

Seven scenes illustrate A's B request, B's return A request, constructor-cycle failure/actual nested exception, fresh acyclic orchestration design, actual tests and recap, then Thanks. Graph movement/reveal times are illustrative edit cues, not runtime-performance measurements. The app register(Acyclic)/refresh→Spring independent A/B→Orchestrator(A,B) overview holds **34.350208–36.350208s** before separate spoken Thanks.120source core frames are identical;120encoded frames checked at120×216,maxmeanRGBvariation0.001350. Actual last frame retained.

## Actual audio and outstanding gate

Local Kokorov1.0,80%am_puck/20%am_fenrir,normal1.02,seven coherent utterances,.08ordinary joins. One entire third scene regenerated to explain arguments must exist before construction; other fresh scene utterances retained. No word splicing, slowdown,time stretching,pitch shift or substituteTTS. Clean narration37.690958s,48kmonoPCM24,onset0.015187s,peak-1.514415dBFS,clipped samples0.

Actual unprompted small.en int8 ASR: 84expected/84observed words,0edits,rawWER0.0000%. This normalized recognition result is not listening approval. Actual waveform hash/model/style checks,dependency lock,phonemes,original segments,ASR timing and signal metrics retained. Naturalness and perceived age remain UNVERIFIED; production is expressly incomplete for this essential requirement.

Quiet original NumPy harmonic music/effects with speech-envelope ducking and two-pass normalization. No sampled third-party song/stock portrait/proprietaryAPI. InterOFL,DejaVu,KokoroApache2.0,inferenceMIT and Java/JUnit license evidence retained. Six official platform-policy sources freshly retrieved with hashes/status/short excerpts. Manual AI disclosure,frame/cover selection,crops/account eligibility and publication approval remain required; monetization is not guaranteed.

Root's actual decoded-image visual review is recorded in qa/visual-review.md; sampled stills only, no every-frame manual watching/listening/browser/phone approval. Local phone-player controls and unchanged media are prepared but unpublished. Independent platform-copy probe/decode/hash and archive/member/manifest checks are recorded by deliver.py after final source/report freeze.
