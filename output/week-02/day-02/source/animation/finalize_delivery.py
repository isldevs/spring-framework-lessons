#!/usr/bin/env python3
"""Finalize frozen reviewed assets, all manifests and ZIPs; never publish."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT.parent
EXCLUDED = {'.venv', 'venv', '__pycache__', 'models'}
REQUIRED = ['video.mp4', 'cover.png', 'first-frame.png', 'thumbnail-style.json',
            'subtitles.srt', 'subtitle-style.json', 'narration.wav', 'narration-script.md',
            'storyboard.md', 'youtube-metadata.md', 'facebook-metadata.md', 'verification-report.md',
            'asset-rights.md', 'originality-review.md', 'platform-policy-review.md',
            'qa/opening-0.0s.png', 'qa/opening-0.5s.png', 'qa/opening-1.0s.png', 'qa/opening-2.0s.png',
            'qa/cover-feed-9x16.png', 'qa/cover-grid-square.png', 'qa/cover-feed-3x4.png',
            'qa/mobile-preview.png', 'qa/qa-summary.json', 'source/animation/render.py',
            'source/animation/validate.py', 'source/animation/opening_qa.py', 'source/animation/package_platforms.py',
            'source/animation/finalize_delivery.py', 'source/animation/audio_mix.py', 'source/voice/generate.py',
            'source/java/run.sh', 'source/rebuild.sh']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    return sorted(path for path in ROOT.rglob('*') if path.is_file() and not path.is_symlink()
                  and not EXCLUDED.intersection(path.relative_to(ROOT).parts)
                  and path.suffix not in {'.pyc', '.pyo'})


def verify_manifest(base, manifest):
    count = 0
    for line in manifest.read_text().splitlines():
        expected, relative = line.split('  ', 1)
        assert digest(base / relative) == expected, relative
        count += 1
    return count


def main():
    qa = json.loads((ROOT / 'source/evidence/final-summary.json').read_text())
    assert digest(ROOT / 'video.mp4') == qa['video_sha256'], 'Master changed after validation'
    for relative, expected in qa['validated_file_sha256'].items():
        assert digest(ROOT / relative) == expected, ('Validated asset changed before finalization', relative)
    platform_qa = json.loads((ROOT / 'source/evidence/platform-validation-summary.json').read_text())
    assert platform_qa['technical_status'] == 'PASS' and platform_qa['master_sha256'] == qa['video_sha256']
    for relative, expected in platform_qa['publishing_metadata_sha256'].items():
        assert digest(ROOT / relative) == expected, ('Publishing metadata changed after packaging', relative)
    for result in platform_qa['results']:
        for relative, expected in result['copied_assets'].items():
            assert digest(ROOT / relative) == expected, ('Master package asset changed after packaging', relative)
            assert digest(ROOT / 'platforms' / result['platform'] / relative) == expected
    for relative in REQUIRED:
        path = ROOT / relative
        assert path.is_file() and path.stat().st_size > 0, relative
    opening = json.loads((ROOT / 'qa/qa-summary.json').read_text())
    for relative in opening.get('required_files', []):
        # QA records lesson-relative paths; refuse paths outside this lesson.
        path = ROOT / relative
        assert path.resolve().is_relative_to(ROOT.resolve()), relative
        assert path.is_file() and path.stat().st_size > 0, relative
    for path in files():
        if path.suffix == '.sh':
            path.chmod(0o755)
    archives = [PARENT / f'{ROOT.name}-{name}-upload.zip' for name in ['youtube-shorts', 'facebook-reels']]
    platforms = []
    for name, archive in zip(['youtube-shorts', 'facebook-reels'], archives):
        folder = ROOT / 'platforms' / name
        count = verify_manifest(folder, folder / 'checksums.sha256')
        assert digest(folder / f'{name}.mp4') == qa['video_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            expected_entries = {f'{name}/{p.name}' for p in folder.iterdir() if p.is_file()}
            assert set(z.namelist()) == expected_entries
            for path in folder.iterdir():
                if path.is_file():
                    assert hashlib.sha256(z.read(f'{name}/{path.name}')).hexdigest() == digest(path)
        platforms.append({'platform': name, 'manifest_files_verified': count,
                          'archive_matches_current_folder': True, 'archive_crc_pass': True})
    platform_hashes = ''.join(digest(path) + '  ' + path.name + '\n' for path in archives)
    (PARENT / f'{ROOT.name}-platform-archives.sha256').write_text(platform_hashes)
    (ROOT / 'platforms/platform-archives.sha256').write_text(platform_hashes)
    manifest = ROOT / 'checksums.sha256'
    members = [path for path in files() if path != manifest]
    manifest.write_text(''.join(digest(path) + '  ' + path.relative_to(ROOT).as_posix() + '\n' for path in members))
    lesson_count = verify_manifest(ROOT, manifest)
    production = PARENT / f'{ROOT.name}-production.zip'
    with zipfile.ZipFile(production, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in files():
            z.write(path, Path(ROOT.name) / path.relative_to(ROOT))
    with zipfile.ZipFile(production) as z:
        assert z.testzip() is None
        expected_entries = {(Path(ROOT.name) / p.relative_to(ROOT)).as_posix() for p in files()}
        assert set(z.namelist()) == expected_entries
        for path in files():
            entry = (Path(ROOT.name) / path.relative_to(ROOT)).as_posix()
            assert hashlib.sha256(z.read(entry)).hexdigest() == digest(path), entry
    archives.append(production)
    archive_manifest = PARENT / f'{ROOT.name}-archives.sha256'
    archive_manifest.write_text(''.join(digest(path) + '  ' + path.name + '\n' for path in archives))
    assert verify_manifest(PARENT, archive_manifest) == 3
    result = {'master_sha256': qa['video_sha256'], 'lesson_manifest_files_verified': lesson_count,
              'required_nonempty_files_verified': len(REQUIRED), 'platforms': platforms,
              'production_archive_crc_pass': True, 'production_archive_matches_current_files': True,
              'archive_hashes_verified': 3,
              'archives': [{'file': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path)} for path in archives],
              'excluded': sorted(EXCLUDED) + ['*.pyc', '*.pyo', 'symlinks'],
              'strict_overall_status': 'INCOMPLETE: perceptual voice acceptance is not certified by technical checks',
              'publication': 'No social upload, scheduling, publication or live preview deployment; manual approval required. Repository file delivery remains separately authorized.'}
    (PARENT / f'{ROOT.name}-delivery-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
