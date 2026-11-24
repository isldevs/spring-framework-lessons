#!/usr/bin/env python3
"""Finalize current reviewed files, manifests and ZIP; never upload or publish."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT.parent
EXCLUDED = {'.venv', 'venv', '__pycache__', 'models'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink()
                  and not EXCLUDED.intersection(p.relative_to(ROOT).parts)
                  and p.suffix not in {'.pyc', '.pyo'})


def verify_manifest(base, manifest):
    count = 0
    for line in manifest.read_text().splitlines():
        expected, relative = line.split('  ', 1)
        assert digest(base / relative) == expected, relative
        count += 1
    return count


def main():
    qa = json.loads((ROOT / 'source/evidence/final-summary.json').read_text())
    assert digest(ROOT / 'video.mp4') == qa['video_sha256']
    required = ['cover.png', 'subtitles.srt', 'narration.wav', 'storyboard.md',
                'narration-script.md', 'youtube-metadata.md', 'facebook-metadata.md',
                'verification-report.md', 'asset-rights.md', 'originality-review.md']
    assert all((ROOT / p).is_file() for p in required)
    for p in files():
        if p.suffix == '.sh':
            p.chmod(0o755)
    platform_results = []
    archives = [PARENT / f'{ROOT.name}-{name}-upload.zip'
                for name in ['youtube-shorts', 'facebook-reels']]
    for name, archive in zip(['youtube-shorts', 'facebook-reels'], archives):
        out = ROOT / 'platforms' / name
        count = verify_manifest(out, out / 'checksums.sha256')
        assert digest(out / f'{name}.mp4') == qa['video_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for p in out.iterdir():
                if p.is_file():
                    assert hashlib.sha256(z.read(f'{name}/{p.name}')).hexdigest() == digest(p)
        platform_results.append({'platform': name, 'manifest_files_verified': count,
                                 'archive_matches_current_folder': True,
                                 'archive_crc_pass': True})
    platform_hashes = ''.join(digest(p) + '  ' + p.name + '\n' for p in archives)
    (PARENT / f'{ROOT.name}-platform-archives.sha256').write_text(platform_hashes)
    (ROOT / 'platforms/platform-archives.sha256').write_text(platform_hashes)
    manifest = ROOT / 'checksums.sha256'
    members = [p for p in files() if p != manifest]
    manifest.write_text(''.join(digest(p) + '  ' + p.relative_to(ROOT).as_posix() + '\n'
                                for p in members))
    count = verify_manifest(ROOT, manifest)
    production = PARENT / f'{ROOT.name}-production.zip'
    with zipfile.ZipFile(production, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files():
            z.write(p, Path(ROOT.name) / p.relative_to(ROOT))
    with zipfile.ZipFile(production) as z:
        assert z.testzip() is None
        for p in files():
            entry = (Path(ROOT.name) / p.relative_to(ROOT)).as_posix()
            assert hashlib.sha256(z.read(entry)).hexdigest() == digest(p), entry
    archives.append(production)
    archive_manifest = PARENT / f'{ROOT.name}-archives.sha256'
    archive_manifest.write_text(''.join(digest(p) + '  ' + p.name + '\n' for p in archives))
    assert verify_manifest(PARENT, archive_manifest) == 3
    result = {'master_sha256': qa['video_sha256'], 'lesson_manifest_files_verified': count,
              'platforms': platform_results, 'production_archive_crc_pass': True,
              'production_archive_matches_current_files': True,
              'archive_hashes_verified': 3,
              'archives': [{'file': p.name, 'bytes': p.stat().st_size, 'sha256': digest(p)}
                           for p in archives],
              'excluded': sorted(EXCLUDED) + ['*.pyc', '*.pyo', 'symlinks'],
              'strict_overall_status': 'INCOMPLETE: perceptual voice review unavailable',
              'publication': 'No YouTube/Facebook upload, scheduling or publication'}
    (PARENT / f'{ROOT.name}-delivery-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
