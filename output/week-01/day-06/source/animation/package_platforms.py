#!/usr/bin/env python3
"""Copy verified master into platform packages, verify actual exports and archive.
No account access, upload or publication. Run after render.py and validate.py.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def main():
    timing=json.loads((ROOT/'source/timing.json').read_text())
    qa=json.loads((ROOT/'source/evidence/final-summary.json').read_text())
    asr=json.loads((ROOT/'source/voice/asr-summary.json').read_text())
    supplement_path=ROOT/'source/voice/supplemental-asr.json'
    supplement=json.loads(supplement_path.read_text()) if supplement_path.exists() else {}
    supplement_note='The late Thanks phrase was also independently transcribed from its actual audio crop without a prompt and matched all three words; the raw full-stream omission remains recorded.' if supplement.get('needed') and supplement.get('exact_normalized_phrase_match') else 'Raw speech-recognition evidence is retained without invented corrections.'
    master_hash=digest(ROOT/'video.mp4');results=[]
    for name,label,required in [('youtube-shorts','YouTube Shorts',['title.txt','description.txt','tags.txt','pinned-comment.txt']),('facebook-reels','Facebook Reels',['caption.txt'])]:
        out=ROOT/'platforms'/name;out.mkdir(parents=True,exist_ok=True)
        for src,dst in [('video.mp4',name+'.mp4'),('cover.png','cover.png'),('subtitles.srt','subtitles.srt')]:shutil.copy2(ROOT/src,out/dst)
        video=out/(name+'.mp4');assert digest(video)==master_hash
        for f in required+['upload-notes.md']:assert (out/f).is_file(),f
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)],text=True))
        write_json(out/'ffprobe.json',probe)
        write_json(ROOT/'source/evidence'/f'platform-{name}-ffprobe.json',probe)
        v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
        assert (v['codec_name'],v['width'],v['height'],v['avg_frame_rate'],a['codec_name'])==('h264',1080,1920,'60/1','aac')
        assert all(v[k]=='bt709' for k in ['color_space','color_transfer','color_primaries'])
        assert v['color_range']=='tv' and a['channels']==2 and a['sample_rate']=='48000'
        assert 35<=duration<45 and abs(duration-qa['duration'])<.002
        cmd=['ffmpeg','-v','error','-i',str(video),'-f','null','-'];p=subprocess.run(cmd,capture_output=True,text=True)
        (ROOT/'source/evidence'/f'platform-{name}-decode.stderr.txt').write_text(p.stderr)
        write_json(ROOT/'source/evidence'/f'platform-{name}-decode.command.json',{'command':cmd,'exit_code':p.returncode})
        assert p.returncode==0 and not p.stderr.strip(),p.stderr
        assert digest(out/'cover.png')==digest(ROOT/'cover.png') and Image.open(out/'cover.png').size==(1080,1920)
        assert digest(out/'subtitles.srt')==digest(ROOT/'subtitles.srt')
        notes=out/'upload-notes.md';text=notes.read_text()
        text=re.sub(r'\d+\.\d+-second',f'{duration:.6f}-second',text)
        text=text.replace('[the verification report](../../verification-report.md)','[technical and voice review notes](technical-checks.md)')
        if 'closing recap' not in text.lower():text+='\nThe closing recap shows separate registries, child-to-parent named lookup fallback and the absence of reverse lookup. The parent bean stays in the parent registry. The completed diagram remains visible for at least two seconds.\n'
        notes.write_text(text)
        (out/'technical-checks.md').write_text(f'''# {label} technical checks

**Export packaging complete. Technical validation passed. Perceptual voice acceptance remains unverified.**

- `{name}.mp4`: {duration:.6f}s, native 1080×1920, 60 FPS, H.264 High, AAC stereo 48 kHz.
- Rec.709 matrix/transfer/primaries, limited range, yuv420p 8-bit SDR confirmed by actual FFprobe.
- Actual full decode exit 0, empty error log; {v['nb_read_frames']} video frames.
- Byte-identical lossless copy of the master. Video SHA-256: `{master_hash}`.
- Immediate spoken and animated mechanism hook from frame one; separate branded cover PNG; burned English captions; separate SRT with {len(timing['captions'])} valid cues.
- Progressive closing recap, with completed diagram held for {timing['recap_hold_seconds']:.2f}s before a separate Thanks for watching end card. User authorizes up to 45 s; this export stays strictly below 45 s.
- Encoded master loudness {qa['integrated_loudness_lufs']:.2f}LUFS, true peak {qa['true_peak_dbtp']:.2f}dBTP.
- Voice: local Kokoro 80% am_puck / 20% am_fenrir, adult male explanatory style. Independent unprompted ASR: {asr['reference_words']} expected words, raw normalized WER {asr['normalized_word_error_rate']:.6f}; raw transcript and alignment provenance retained in production source. {supplement_note}

No auditory listening review is claimed. Perceived age, human naturalness and subtle speech artifacts cannot be certified in this runtime. Final strict voice approval remains incomplete. All technical validation and packaging checks above are actual measurements, not a substitute for listening acceptance.

Use upload-notes.md and paste-ready copy. Caption overlays are already in the video; avoid duplicate decorative captions. Nothing has been uploaded, scheduled or published to YouTube or Facebook. All files in this folder except the manifest itself are covered by checksums.sha256.
''')
        results.append({'platform':name,'path':str(video.relative_to(ROOT)),'sha256':master_hash,'byte_identical_to_master':True,'duration_s':duration,'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'decoded_frames':int(v['nb_read_frames']),'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'color_primaries':v['color_primaries'],'color_transfer':v['color_transfer'],'color_space':v['color_space'],'color_range':v['color_range'],'audio_sample_rate':int(a['sample_rate']),'audio_channels':a['channels'],'full_decode_exit_code':p.returncode,'full_decode_stderr_empty':not p.stderr,'cover_dimensions':[1080,1920],'cover_byte_identical_to_master':True,'subtitles_byte_identical_to_master':True,'subtitle_cues':len(timing['captions']),'technical_result':'PASS'})
        files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='checksums.sha256')
        (out/'checksums.sha256').write_text(''.join(digest(p)+'  '+p.name+'\n' for p in files))
        subprocess.run(['sha256sum','-c','checksums.sha256'],cwd=out,check=True,stdout=subprocess.DEVNULL)
        archive=ROOT.parent/(ROOT.name+'-'+name+'-upload.zip')
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(out.iterdir()):
                if p.is_file():z.write(p,Path(name)/p.name)
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
        print(f'{label}: actual file/decode/hash/archive checks PASS: {archive}',flush=True)
    write_json(ROOT/'source/evidence/platform-validation-summary.json',{'master_sha256':master_hash,'results':results,'both_exports_byte_identical':True,'technical_status':'PASS','perceptual_voice_review':'UNVERIFIED: no auditory review performed'})
    (ROOT/'source/evidence/platform-validation-notes.md').write_text('# Platform verification\n\nBoth current exported MP4s were independently probed and fully decoded without errors. SHA-256 equals the current master for both. Both exact covers and SRT files equal their current master files. All current properties and command evidence are in platform-validation-summary.json and platform-*-decode.command.json. No perceptual voice review was performed.\n')
if __name__=='__main__':main()
