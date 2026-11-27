from pathlib import Path
import subprocess,json,re,hashlib
import numpy as np
r=Path(__file__).resolve().parents[2];d=json.loads((r/'source/timing.json').read_text());first=int(np.ceil(d['recap_hold_start']*60));last=first+120
cmd=['ffmpeg','-v','error','-i',str(r/'video.mp4'),'-vf',f'select=between(n\\,{first}\\,{last-1}),scale=120:216','-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-']
p=subprocess.run(cmd,capture_output=True,check=True);frames=np.frombuffer(p.stdout,np.uint8).reshape(-1,216,120,3);assert len(frames)==120
errors=np.abs(frames.astype(float)-frames[0].astype(float)).mean(axis=(1,2,3));assert errors.max()<2
p=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','frame=best_effort_timestamp_time','-of','csv=p=0',str(r/'video.mp4')],capture_output=True,text=True,check=True);pts=[float(x.split(',')[0]) for x in p.stdout.splitlines() if x.strip()];assert len(pts)==2171 and all(abs(v-i/60)<.00001 for i,v in enumerate(pts))
(r/'source/evidence/frame-timestamps.txt').write_text(p.stdout)
(r/'qa/additional-checks.json').write_text(json.dumps({'encoded_recap_frames_checked':len(frames),'recap_comparison':'120x216 decoded RGB samples, all120frames','max_mean_rgb_difference_from_first':float(errors.max()),'timestamps_checked':len(pts),'constant60fps':True,'scope':'Automated continuity checks, not auditory acceptance.'},indent=2))
q=json.loads((r/'source/evidence/final-summary.json').read_text());v=json.loads((r/'source/voice/qa-metrics.json').read_text());a=json.loads((r/'source/voice/asr-summary.json').read_text());j=json.loads((r/'source/evidence/java-verification-result.json').read_text())
(r/'verification-report.md').write_text(f'''# Verification — Optional dependencies

**Production INCOMPLETE for perceptual listening acceptance.** A real narrated MP4 and supporting files are delivered; no supported auditory review was available. Smoothness, pronunciation, rhythm and perceived age remain unverified. Browser and physical-phone playback remain untested. No automatic upload, scheduling, cover selection or live-player deployment occurred.

Approved topic Optional dependencies; publication **2026-11-25**, proposed **19:00 Asia/Phnom_Penh** (12:00UTC), unchanged despite later production. No public week/day/episode numbering.

## Actual export

- {q['duration']:.6f}s, native1080×1920,60FPS,{q['frames']}frames; H.264/AAC stereo48kHz,8-bit yuv420p,Rec.709SDR. FFprobe raw JSON retained.
- Full decode passed with empty error log,0black intervals. Actual fast-start moov precedes mdat. All2171frame timestamps checked at60FPS.
- Final measured loudness {q['loudness']['input_i']}LUFS/{q['loudness']['input_tp']}dBTP. Audio silence log retained; listening acceptance is not inferred from signal checks.
- Master SHA256 `{q['sha256']}`.

## Actual Java/Spring tests

**4/4 JUnit tests passed**,0failures/skips. ECJ3.40 targetsJava17 onactualJDK21.0.13; Spring/spring-test6.2.11,JUnit5.12.2/platform1.12.2;11pinned dependency JARs with checksums/licenses. Main/test compile and JUnit exit0. Expected warnings from two deliberately failing context refreshes are retained in stderr. Two tested Java source hashes were rechecked by media validation.

Three requested cases plus an ambiguity guard genuinely ran. RequiredService(AuditPublisher) without a candidate fails refresh with UnsatisfiedDependencyException/rootNoSuchBeanDefinitionException. OptionalService(Optional<AuditPublisher>) without a candidate starts with Optional.empty() and notification safely skipped. With one candidate it starts and assertSame confirms the exact managed publisher reference. Two competing candidates still fail refresh with rootNoUniqueBeanDefinitionException. No standalone app/business/security compliance coverage is claimed.

Actual proof lines:

```text
{chr(10).join(j['proof_lines'])}
```

Current official Spring6.2 reference and6.2.11Autowired API returnedHTTP200; hashes/pages/excerpt retained. The reference explicitly permits java.util.Optional to express a non-required dependency. Optional handles absence, not every resolution error. Critical security dependencies should not be made optional to bypass startup failure. The audit publisher shown here is an extra notification feature, not a security guarantee.

## Opening, layout and captions

Inter variable900/opsz32,104px,white multiline headline Missing Bean? / Spring Can / Still Start. Only Missing Bean? is blue#0866FF,20px rounded,18/8padding. Font license/provenance retained. The cover equals source frame0 exactly. All61headlineROI samples0–1s are stable; meaningful technical motion starts1/60s. Transition1–2s carries the technical card upward while retiring the cover headline. Separate hook caption exactly matches speech. Actual encoded0/.5/1/1.25/1.5/1.75/2s images were compared with source; frame0 meanRGBerror{q['opening'][0]['mean_absolute_rgb_error']:.6f}. Lossy decoded pixel identity is not claimed.

Pillow textbbox and RGBA captions: Inter700/52px,white,blackalpha209≈82%,radius12,padding26/14,dynamicwidth≤840,center540/1380,max2lines.17coherent cues,3–7words each; actual final script words. Source preflight250states found zero safe-bound violations insideX90..990/Y250..1520. Separate SRT uses actual observed Whisper word spans and sample-derived scene edges, not evenly divided estimates. Known-input AuditPublisher compound mapping retains the raw recognition data.

Seven purposeful scenes: required lookup/failure, Optional constructor/nested type, present managed reference, absent empty value, actual tests/qualification/recap and Thanks, preceded by full-cover moving hook. The complete app→Config/refresh→Spring nested-type resolution→Optional→service recap holds32.839208–34.839208s before separate spoken Thanks.120source frames are identical;120encoded frames were checked at120×216 with maxmeanRGBdifference{errors.max():.6f}. No runtime-performance claim is made.

## Narration, rights and limitations

Fresh local Kokorov1.0,80%am_puck/20%am_fenrir,normal1.02,seven coherent utterances,.08joins,2srecap hold. Actual clean narration{d['duration']:.6f}s,48kmonoPCM24. Speech onset{v['speech_above_minus60db_onset_s']:.6f}s,peak{v['peak_dbfs']:.6f}dBFS,clipped samples{v['clipped_samples']}. Raw unprompted small.en:78reference/79observedwords,2edits,WER2.5641%,only AuditPublisher→audit publisher compound spacing. No fake zero-WER or auditory approval. Models/style hashes/licenses/setup/lock/segments/phonemes and provenance retained; no substituteTTS,time/pitch manipulation or isolated-word splicing.

Original quiet NumPy harmonic music/effects, speech ducking and two-pass normalization. InterOFL,DejaVu,KokoroApache2.0,inferenceMIT and Java/JUnit licenses retained; no stock portrait/third-party sampled song/proprietary API. Six official platform-policy sources freshly fetched with status/hash/bounded excerpts. Manual disclosure controls, frame/cover selection, crop/account approval and monetization review remain owner tasks. No monetization guarantee.

Root visually inspected actual firstframe, encodedseven-scene contact, transition sample, squarecrop and actuallastframe; final reviewed image list is retained in qa/visual-review.md. Main text/captions are readable in those samples; supporting labels smaller. This is sampled still-image review, not every-frame viewing or device playback. Phone player source/media are prepared locally and remain unpublished pending manual approval. Independent packaged-copy probe/decode/hash checks and finalZIP/manifest validation are recorded separately by deliver.py after freeze. No check is implied solely by a file existing.
''')
print('Additional encoded hold/timestamps passed; actual report written')
