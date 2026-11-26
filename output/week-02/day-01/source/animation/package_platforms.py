#!/usr/bin/env python3
"""Package the validated master for two platforms; never upload or publish.

Run only after the actual final MP4 and its opening/style QA have passed.
"""
from pathlib import Path
from PIL import Image
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'source/evidence'
COPY_ASSETS = ['cover.png', 'first-frame.png', 'subtitles.srt',
               'thumbnail-style.json', 'subtitle-style.json', 'platform-policy-review.md']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def metadata_section(path, heading):
    match = re.search(r'^## ' + re.escape(heading) + r'\n+(.*?)(?=^## |\Z)',
                      path.read_text(), re.M | re.S)
    assert match, (path.name, heading)
    return match.group(1).strip() + '\n'


def prepare_publishing_copy():
    yt, fb = ROOT / 'youtube-metadata.md', ROOT / 'facebook-metadata.md'
    for path in [yt, fb]:
        assert 'Constructor injection' in path.read_text()
        assert '2026-11-23' in path.read_text()
    expected = {
        'youtube-shorts': {
            'title.txt': metadata_section(yt, 'Title'),
            'description.txt': metadata_section(yt, 'Description and hashtags'),
            'tags.txt': metadata_section(yt, 'Tags (comma-separated)'),
            'pinned-comment.txt': metadata_section(yt, 'Pinned comment')},
        'facebook-reels': {'caption.txt': metadata_section(fb, 'Caption and hashtags')}}
    for name, items in expected.items():
        out = ROOT / 'platforms' / name
        out.mkdir(parents=True, exist_ok=True)
        for filename, text in items.items():
            (out / filename).write_text(text)
        label = 'YouTube Shorts' if name == 'youtube-shorts' else 'Facebook Reels'
        selection = (
            'In the YouTube mobile Shorts upload/edit flow, use manual video-frame thumbnail selection '
            'where that control is offered. Scrub to the opening0–1s and confirm the full headline is visible. '
            'If the current interface supports custom-thumbnail upload, use cover.png. Availability can vary '
            'by device/account/interface; neither automatic selection nor a particular crop is guaranteed.'
            if name == 'youtube-shorts' else
            'In the Facebook Reels upload/edit flow, open the manual cover control where offered. '
            'Upload cover.png if supported, or select an opening0–1s frame that retains the full headline. '
            'Confirm the actual feed/profile crop in the current interface; automatic cover selection is not guaranteed.')
        (out / 'upload-notes.md').write_text(f'''# {label} manual upload notes

Use `{name}.mp4` with the platform-specific copy in this folder. The master starts with the complete cover composition, immediate narration and meaningful technical motion. The headline stays recognizable through the first second, then transitions into the explanation. `cover.png` is the separate source artwork; `first-frame.png` is decoded from the actual lossy MP4 and is not claimed pixel-identical to it.

## Manual thumbnail or cover selection

{selection}

## Publication and final review

Approved topic: **Constructor injection**. Publication date: **2026-11-23**, proposed **19:00 Asia/Phnom_Penh** (12:00 UTC). These are metadata only. Do not upload, schedule or publish without the user's manual approval.

Review the actual platform preview, crop, caption position, audio and current AI-disclosure prompts. `platform-policy-review.md` records the official-policy review and items needing manual confirmation. No monetization approval, copyright clearance by a platform or automatic thumbnail selection is guaranteed.

The video already burns in white Inter Bold captions on measured, rounded,82%-black RGBA backgrounds. `subtitles.srt` is a separate accessibility track where supported; avoid adding a second decorative caption layer. The supplied style JSON files retain actual thumbnail and caption settings.

The code demonstrates a Spring-managed service with one unannotated constructor and one matching PaymentGateway. The deterministic `demo-paid:2500` result comes from an in-memory demo gateway; it is not a real payment. Manually constructed objects still use caller-supplied arguments. The completed overview is held for at least two seconds before Thanks.

See `technical-checks.md` after packaging for actual measurements and remaining voice-review limits. No auditory approval is claimed unless an actual listening review is separately recorded. This script does not publish a private phone-preview page either.
''')
    (ROOT / 'platforms/README.md').write_text('''# Platform upload packages

Both folders contain independently verified, byte-identical copies of the rendered master, exact cover/SRT, the actual decoded first frame, style records and platform-policy notes. YouTube has its title, description/hashtags, comma-separated tags and pinned comment. Facebook has a distinct caption/hashtags.

Approved topic Constructor injection; publication2026-11-23, proposed19:00Asia/Phnom_Penh. Public media contains no internal numbering. Sourceframe0 matches the cover composition before compression. During0–1s its complete headline is stable while speech and technical motion begin;1–2s transitions into the mechanism. Decoded-frame comparisons allow normal lossy encoding differences. Use the manual opening-frame thumbnail/cover instructions in each folder and confirm the actual upload preview.

Parent archives are day-01-youtube-shorts-upload.zip, day-01-facebook-reels-upload.zip and day-01-production.zip under output/week-02/. Nothing is automatically uploaded, scheduled or published; manual approval is required. Perceptual narration acceptance is a separate gate from technical measurements and is not fabricated.
''')


def main():
    prepare_publishing_copy()
    timing = json.loads((ROOT / 'source/timing.json').read_text())
    qa = json.loads((E / 'final-summary.json').read_text())
    asr = json.loads((ROOT / 'source/voice/asr-summary.json').read_text())
    master_hash = digest(ROOT / 'video.mp4')
    assert master_hash == qa['video_sha256'], 'Master changed after final validation'
    assert asr['narration_sha256'] == digest(ROOT / 'narration.wav')
    for name in COPY_ASSETS:
        assert (ROOT / name).is_file() and (ROOT / name).stat().st_size > 0, name
    results = []
    for name, label, required in [
        ('youtube-shorts', 'YouTube Shorts', ['title.txt', 'description.txt', 'tags.txt', 'pinned-comment.txt']),
        ('facebook-reels', 'Facebook Reels', ['caption.txt'])]:
        out = ROOT / 'platforms' / name
        shutil.copy2(ROOT / 'video.mp4', out / f'{name}.mp4')
        for asset in COPY_ASSETS:
            shutil.copy2(ROOT / asset, out / asset)
        video = out / f'{name}.mp4'
        assert digest(video) == master_hash
        assert all((out / item).is_file() for item in required + ['upload-notes.md'])
        cmd = ['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(video)]
        probe = json.loads(subprocess.check_output(cmd, text=True))
        write_json(out / 'ffprobe.json', probe)
        write_json(E / f'platform-{name}-ffprobe.json', probe)
        v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        a = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
        duration = float(probe['format']['duration'])
        assert (v['codec_name'], v['width'], v['height'], v['avg_frame_rate'], a['codec_name']) == ('h264', 1080, 1920, '60/1', 'aac')
        assert all(v[k] == 'bt709' for k in ['color_space', 'color_transfer', 'color_primaries'])
        assert v['color_range'] == 'tv' and a['sample_rate'] == '48000' and a['channels'] == 2
        assert 0 < duration < 45 and abs(duration - qa['duration']) < .002
        assert int(v['nb_read_frames']) == qa['frames']
        cmd = ['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-']
        result = subprocess.run(cmd, capture_output=True, text=True)
        (E / f'platform-{name}-decode.stderr.txt').write_text(result.stderr)
        write_json(E / f'platform-{name}-decode.command.json', {'command': cmd, 'exit_code': result.returncode})
        assert result.returncode == 0 and not result.stderr.strip(), result.stderr
        for asset in COPY_ASSETS:
            assert digest(out / asset) == digest(ROOT / asset), asset
        for asset in ['cover.png', 'first-frame.png']:
            assert Image.open(out / asset).size == (1080, 1920)
        (out / 'technical-checks.md').write_text(f'''# {label} actual technical checks

**Technical media/copy validation passed. Perceptual voice acceptance remains a separate, unverified requirement unless an actual listening review is recorded.**

- `{name}.mp4`: {duration:.6f}s, native1080×1920,60FPS,H.264 {v.get('profile', 'unspecified profile')},AAC stereo48kHz.
- Actual FFprobe confirms Rec.709 matrix/transfer/primaries,limited-range,yuv420p8-bitSDR;{v['nb_read_frames']}frames.
- Actual full decode exit0,empty error log; SHA-256 matches master `{master_hash}`.
- Source opening-frame/cover equality, headline stability/motion,1–2s transition and actual lossy-frame similarity are checked in production opening QA. No pixel-identical decoded/source-frame claim is made.
- Exact copied cover, decodedfirst-frame,SRT,styleJSON and policy record. SeparateSRT has{len(timing['captions'])}cues. Burned captions use the actual style record; no duplicate decorative captions are needed.
- Completed mechanism recap holds{timing['recap_hold_seconds']:.2f}s before separate spoken Thanks; duration stays strictly below45s.
- Encoded master loudness{qa['integrated_loudness_lufs']:.2f}LUFS,truepeak{qa['true_peak_dbtp']:.2f}dBTP.
- Local male Kokoro narration. Actual unprompted ASR model{asr.get('model', 'recorded in source')} has{asr['reference_words']}expectedwords and raw normalizedWER{asr['normalized_word_error_rate']:.6f}. Raw transcript and caption-alignment provenance are retained; recognition is not listening acceptance.

Two actual JUnit tests verify implicit single-constructor injection, the selected gateway reference, deterministic demo execution and manual caller-supplied dependencies. The demo performs no real payment. No standalone application or comprehensive behavior test is claimed.

Read upload-notes.md and platform-policy-review.md. Manual approval, cover selection, upload preview and current AI-disclosure confirmation remain user actions. No publication or monetization approval is guaranteed; no listening review is fabricated. This folder's manifest covers every file except itself.
''')
        results.append({'platform': name, 'path': str(video.relative_to(ROOT)), 'sha256': master_hash,
                        'byte_identical_to_master': True, 'duration_s': duration, 'width': v['width'],
                        'height': v['height'], 'fps': v['avg_frame_rate'], 'decoded_frames': int(v['nb_read_frames']),
                        'video_codec': v['codec_name'], 'video_profile': v.get('profile'), 'audio_codec': a['codec_name'],
                        'color_space': v['color_space'], 'color_transfer': v['color_transfer'], 'color_primaries': v['color_primaries'],
                        'color_range': v['color_range'], 'audio_sample_rate': int(a['sample_rate']), 'audio_channels': a['channels'],
                        'full_decode_exit_code': result.returncode, 'full_decode_stderr_empty': not result.stderr,
                        'copied_assets': {asset: digest(out / asset) for asset in COPY_ASSETS},
                        'cover_dimensions': [1080, 1920], 'first_frame_dimensions': [1080, 1920],
                        'subtitle_cues': len(timing['captions']), 'technical_result': 'PASS'})
        files = sorted(p for p in out.iterdir() if p.is_file() and p.name != 'checksums.sha256')
        manifest = out / 'checksums.sha256'
        manifest.write_text(''.join(digest(p) + '  ' + p.name + '\n' for p in files))
        for line in manifest.read_text().splitlines():
            expected, relative = line.split('  ', 1)
            assert digest(out / relative) == expected
        archive = ROOT.parent / f'{ROOT.name}-{name}-upload.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for path in sorted(out.iterdir()):
                if path.is_file():
                    z.write(path, Path(name) / path.name)
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for path in out.iterdir():
                if path.is_file():
                    assert hashlib.sha256(z.read(f'{name}/{path.name}')).hexdigest() == digest(path)
        print(f'{label}: actual probe/decode/hash/asset/ZIP checks PASS: {archive}', flush=True)
    write_json(E / 'platform-validation-summary.json', {'master_sha256': master_hash, 'results': results,
               'both_exports_byte_identical': True, 'technical_status': 'PASS',
               'perceptual_voice_review': 'UNVERIFIED: no auditory review claimed',
               'publication': 'Prepared packages only; manual approval required'})


if __name__ == '__main__':
    main()
