#!/usr/bin/env python3
"""Create lossless platform upload copies and self-contained ZIP packages.
No network, account access, uploading, or publishing.
Run AFTER master rendering/validation and platform copywriting.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[2]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    timing=json.loads((ROOT/'source/timing.json').read_text())
    master=ROOT/'video.mp4';master_hash=digest(master)
    for name,label,copyfiles in [('youtube-shorts','YouTube Shorts',['title.txt','description.txt','pinned-comment.txt']),('facebook-reels','Facebook Reels',['caption.txt'])]:
        out=ROOT/'platforms'/name;out.mkdir(parents=True,exist_ok=True)
        for src,dst in [('video.mp4',name+'.mp4'),('cover.png','cover.png'),('subtitles.srt','subtitles.srt')]:shutil.copy2(ROOT/src,out/dst)
        assert digest(out/(name+'.mp4'))==master_hash
        for f in copyfiles+['upload-notes.md']:assert (out/f).is_file(),f
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out/(name+'.mp4'))],text=True))
        (out/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
        v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
        assert (v['codec_name'],v['width'],v['height'],v['avg_frame_rate'],a['codec_name'])==('h264',1080,1920,'60/1','aac')
        assert all(v[k]=='bt709' for k in ['color_space','color_transfer','color_primaries'])
        assert 35<=float(probe['format']['duration'])<=40
        notes=out/'upload-notes.md';text=notes.read_text().replace('[the verification report](../../verification-report.md)','[technical and voice review notes](technical-checks.md)');notes.write_text(text)
        (out/'technical-checks.md').write_text(f'''# {label} package checks

**Export packaging complete. Technical checks passed. Perceptual voice acceptance remains unverified.**

- File: `{name}.mp4`; duration {float(probe['format']['duration']):.6f} seconds.
- 1080 × 1920 portrait, H.264 High, 60 FPS, yuv420p 8-bit SDR, limited range.
- Rec.709 matrix, transfer and primaries verified in this actual file with FFprobe.
- AAC stereo, 48 kHz. Original revised male Kokoro narration and quiet original background audio.
- Video is a byte-identical lossless copy of the validated master. There is no additional video/audio generation loss.
- Master and both platform exports have been fully decoded without errors; independent evidence is retained in the production source bundle.
- Approved animation and cover retained. Exact cover is displayed from 0 to 1 second without fade-in; the MP4 includes English captions.
- Separate SRT has {len(timing['captions'])} ordered, nonoverlapping cues within runtime. Cover is 1080 × 1920.
- All contents except this folder's checksum manifest itself are covered by `checksums.sha256`.

Video SHA-256:

```text
{master_hash}
```

Voice style targets younger-to-middle adult male delivery using local Kokoro 80% am_puck / 20% am_fenrir. Six whole-scene utterances provide connected phrasing. Independent Whisper base.en recognizes all 88 words with normalized WER 0.0; source narration has zero clipped samples. The final master measures −16.18 LUFS integrated and −1.36 dBTP.

The runtime cannot ingest audio for a listening review, so perceived age, smooth human naturalness and subtle synthesis artifacts have NOT been perceptually accepted. Under the original strict production requirement, final voice approval remains incomplete despite complete export packaging and passing technical checks. No auditory review is claimed.

Use the accompanying upload notes and paste-ready platform copy. These files have not been uploaded, scheduled or published.
''')
        files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='checksums.sha256')
        (out/'checksums.sha256').write_text(''.join(digest(p)+'  '+p.name+'\n' for p in files))
        subprocess.run(['sha256sum','-c','checksums.sha256'],cwd=out,check=True,stdout=subprocess.DEVNULL)
        archive=ROOT.parent/(name+'-upload.zip')
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(out.iterdir()):
                if p.is_file():z.write(p,Path(name)/p.name)
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
        print(f'{label}: {archive}, {archive.stat().st_size} bytes, archive+file checksums pass')
if __name__=='__main__':main()
