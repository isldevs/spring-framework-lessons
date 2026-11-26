#!/usr/bin/env python3
"""Verify the real constructor-injection thumbnail opening and caption geometry.

Called only against a completed encoded MP4. Source equality is lossless; decoded
comparisons deliberately use similarity and never claim H.264 pixel identity.
"""
from pathlib import Path
import hashlib
import json
import math
import re

import numpy as np
from PIL import Image, ImageFont


def normalized_hex(value):
    return str(value).upper()


def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def safe(box):
    return box[0] >= 90 and box[1] >= 250 and box[2] <= 990 and box[3] <= 1520


def font_asset(root, style):
    path = Path(style['font_file'])
    if not path.is_absolute():
        path = root / path
    assert path.is_file(), path
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == style['font_sha256'], ('Font hash mismatch', path)
    family, face = ImageFont.truetype(str(path), 52).getname()
    assert 'Inter' in family, ('Actual font family', family)
    license_path = root / 'source/assets/Inter-OFL.txt'
    assert license_path.is_file() and 'SIL OPEN FONT LICENSE' in license_path.read_text()
    return {'file': str(path.relative_to(root)), 'sha256': actual,
            'actual_family': family, 'base_face': face,
            'license_file': 'source/assets/Inter-OFL.txt'}


def style_checks(root, renderer, data):
    thumb = json.loads((root / 'thumbnail-style.json').read_text())
    sub = json.loads((root / 'subtitle-style.json').read_text())
    assert 'Inter' in thumb['font_family'] and 800 <= thumb['font_weight'] <= 900
    assert 88 <= thumb['font_size'] <= 120
    assert all(88 <= size <= 120 for size in thumb.get('font_sizes', [thumb['font_size']]))
    assert normalized_hex(thumb['text_color']) == '#FFFFFF'
    assert thumb['headline_lines'] == ['Spring Injection', 'No @Autowired?', 'It still works.']
    highlight = thumb['highlight']
    assert normalized_hex(highlight['background']) == '#0866FF'
    assert highlight['corner_radius'] == 20 and highlight['padding'] == [18, 8]
    assert safe(thumb['headline_bounds'])
    highlighted = next(item['bbox'] for item in thumb['headline_line_bounds']
                       if item['text'] == 'No @Autowired?')
    assert safe([highlighted[0] - 18, highlighted[1] - 8,
                 highlighted[2] + 18, highlighted[3] + 8])
    assert 'Inter' in sub['font_family'] and 700 <= sub['font_weight'] <= 800
    assert 48 <= sub['font_size'] <= 56
    assert normalized_hex(sub['text_color']) == '#FFFFFF'
    assert normalized_hex(sub['background']['color']) == '#000000'
    assert abs(sub['background']['opacity'] - .82) <= 1 / 255
    assert sub['background']['corner_radius'] == 12
    assert sub['padding'] == [26, 14] and sub['max_width'] == 840
    assert sub['center'] == [540, 1380] and sub['max_lines'] == 2
    assert safe(sub['caption_region'])
    fonts = [font_asset(root, x) for x in (thumb, sub)]
    assert hasattr(renderer, 'caption_layout'), 'Renderer must expose measured caption layout'
    records = []
    for cue in data['captions']:
        layout = renderer.caption_layout(cue['text'])
        rect = list(map(float, layout['rect']))
        assert safe(rect) and rect[2] - rect[0] <= 840
        assert abs((rect[0] + rect[2]) / 2 - 540) <= 1
        assert abs((rect[1] + rect[3]) / 2 - 1380) <= 1
        assert 1 <= len(layout['text_lines']) <= 2
        assert layout['font_size'] == sub['font_size']
        assert 700 <= layout['weight'] <= 800
        assert layout['padding'] == [26, 14]
        assert abs(layout['opacity'] - .82) <= 1 / 255
        bounds = layout['text_bounds']
        if len(bounds) == 4 and isinstance(bounds[0], (int, float)):
            bounds = [bounds]
        assert bounds
        for box in bounds:
            assert safe(box) and not (box[0] < rect[0] + 25 or box[2] > rect[2] - 25), (cue, layout)
            assert box[1] >= rect[1] + 13 and box[3] <= rect[3] - 13
        assert not intersects(rect, thumb['headline_bounds']), 'Caption overlaps thumbnail headline'
        # Probe the actual alpha-compositing function on a known nonblack base.
        image = Image.new('RGB', (1080, 1920), (120, 80, 40))
        result = renderer.caption(image, cue['text'])
        if isinstance(result, Image.Image):
            image = result
        pixel = image.convert('RGB').getpixel((round(rect[0] + 13), round((rect[1] + rect[3]) / 2)))
        alpha = round(.82 * 255) / 255
        expected = tuple(round(c * (1 - alpha)) for c in (120, 80, 40))
        assert max(abs(a - b) for a, b in zip(pixel, expected)) <= 2, ('Caption background alpha/color', pixel, expected)
        corner = image.convert('RGB').getpixel((round(rect[0]), round(rect[1])))
        assert corner == (120, 80, 40), ('Caption corner is not rounded', corner)
        # The opening headline/background has its own disjoint reserved regions.
        # Later states are checked before caption compositing, so hidden code is
        # not wrongly accepted merely because the caption paints over it.
        t = (cue['start'] + cue['end']) / 2
        if t >= 2:
            raw = np.asarray(renderer.render_frame(t, data, with_caption=False).convert('RGB'))
            x1, y1, x2, y2 = map(round, rect)
            assert not np.any(raw[y1:y2, x1:x2].max(axis=2) >= 90), ('Bright technical content beneath caption', cue)
        records.append({'text': cue['text'], 'rect': rect, 'text_bounds': bounds,
                        'lines': len(layout['text_lines']), 'font_size': layout['font_size'],
                        'word_count': len(cue['text'].split()),
                        'preferred_3_7_words': 3 <= len(cue['text'].split()) <= 7,
                        'actual_black_alpha_probe': list(pixel)})
    assert len({round(r['rect'][2] - r['rect'][0], 2) for r in records}) > 1, 'Captions must follow text width'
    return thumb, sub, {'fonts': fonts, 'captions': records, 'measured_layouts_passed': True,
                        'preferred_phrase_lengths_all': all(r['preferred_3_7_words'] for r in records),
                        'scope': 'Measured glyph/rectangle bounds, actual alpha-compositing probe and source underlay check; not auditory acceptance.'}


def validate_opening(root, renderer, data, run, parse_ssim):
    evidence = root / 'source/evidence'
    qa = root / 'qa'
    qa.mkdir(parents=True, exist_ok=True)
    video = root / 'video.mp4'
    thumb, sub, caption_record = style_checks(root, renderer, data)
    cover = Image.open(root / 'cover.png').convert('RGB')
    assert cover.size == (1080, 1920)
    first_source = renderer.render_frame(0, data).convert('RGB')
    assert np.array_equal(np.asarray(first_source), np.asarray(cover)), 'Source frame0 differs from cover.png'
    hook = data['phrases'][0]
    assert hook['text'] == 'No Autowired? This still works.' and hook['start'] == 0
    assert data['captions'][0]['text'] == hook['text']
    assert data['captions'][0]['start'] == 0 and abs(data['captions'][0]['end'] - hook['end']) < 1e-6
    headline_roi = tuple(thumb['headline_roi'])
    technical_roi = tuple(thumb['technical_roi'])
    assert safe(headline_roi) and safe(technical_roi)
    assert not intersects(headline_roi, technical_roi)
    assert not intersects(sub['caption_region'], headline_roi)
    assert not intersects(sub['caption_region'], technical_roi)
    headline = np.asarray(cover.crop(headline_roi))
    background = np.asarray(cover.crop(technical_roi))
    changes = []
    hashes = []
    first_change = None
    for frame in range(61):
        image = renderer.render_frame(frame / 60, data).convert('RGB')
        assert np.array_equal(np.asarray(image.crop(headline_roi)), headline), ('Headline moved before 1s', frame)
        core = np.asarray(image.crop(technical_roi))
        count = int(np.any(core != background, axis=2).sum())
        changes.append(count)
        hashes.append(hashlib.sha256(core.tobytes()).hexdigest())
        if frame and count and first_change is None:
            first_change = frame / 60
    assert first_change is not None and first_change < .15
    assert len(set(hashes)) >= 12 and max(changes) >= 100, ('Technical opening motion absent', len(set(hashes)), max(changes))
    transition = []
    previous = np.asarray(renderer.render_frame(1, data).convert('RGB'), dtype=np.int16)
    for frame in range(61, 122):
        current = np.asarray(renderer.render_frame(frame / 60, data).convert('RGB'), dtype=np.int16)
        delta = float(np.abs(current - previous).mean())
        transition.append({'frame': frame, 'time_s': frame / 60, 'mean_absolute_rgb_delta': delta})
        previous = current
    assert max(r['mean_absolute_rgb_delta'] for r in transition) < 20, 'Opening transition has a large one-frame jump'
    actuals = []
    thumbs = []
    for frame in [0, 15, 30, 60, 75, 90, 105, 120]:
        t = frame / 60
        source = evidence / f'final-opening-source-{frame}.png'
        decoded = evidence / f'final-opening-decoded-{frame}.png'
        stats = evidence / f'final-opening-{frame}-ssim-frames.txt'
        renderer.render_frame(t, data).save(source)
        run(['ffmpeg', '-y', '-hide_banner', '-nostats', '-i', str(video),
             '-loop', '1', '-framerate', '60', '-i', str(source), '-filter_complex',
             f'[0:v]trim=start_frame={frame}:end_frame={frame + 1},setpts=PTS-STARTPTS[actual];'
             '[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[expected];'
             f'[actual][expected]ssim=stats_file={stats}[checked]', '-map', '[checked]',
             '-frames:v', '1', '-an', str(decoded)], f'opening-{frame}-ssim')
        similarity = parse_ssim(stats)
        assert len(similarity) == 1 and similarity[0] > .99, (frame, similarity)
        actuals.append({'frame': frame, 'time_s': t, 'source_ssim': similarity[0], 'decoded_image': decoded.name})
        if frame in [0, 30, 60, 120]:
            path = qa / f'opening-{t:.1f}s.png'
            Image.open(decoded).save(path)
        if frame in [75, 90, 105]:
            Image.open(decoded).save(qa / f'transition-{t:.2f}s.png')
        if frame in [0, 30, 60, 75, 90, 120]:
            thumbs.append(Image.open(decoded).resize((270, 480), Image.Resampling.LANCZOS))
    # This standalone frame is an actual decode of encoded frame0, not a copy
    # of the uncompressed cover. Its equality to H.264 input is not claimed.
    run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(video),
         '-frames:v', '1', str(root / 'first-frame.png')], 'first-frame-extract')
    first_decoded = Image.open(root / 'first-frame.png').convert('RGB')
    assert first_decoded.size == (1080, 1920)
    pixel_delta = np.abs(np.asarray(cover, dtype=np.int16) - np.asarray(first_decoded, dtype=np.int16))
    first_metrics = {'mean_absolute_rgb_error': float(pixel_delta.mean()),
                     'maximum_channel_error': int(pixel_delta.max()),
                     'source_frame0_equals_cover_pixels': True,
                     'encoded_frame0_source_ssim': actuals[0]['source_ssim'],
                     'lossy_decoded_pixel_identity_claimed': False}
    mobile = Image.new('RGB', (810, 960), '#090F20')
    for i, image in enumerate(thumbs):
        mobile.paste(image, (i % 3 * 270, i // 3 * 480))
    mobile.save(qa / 'mobile-preview.png')
    mobile.save(evidence / 'final-opening-mobile-contact.png')
    crops = {'cover-feed-9x16.png': ((0, 0, 1080, 1920), (360, 640)),
             'cover-grid-square.png': ((0, 420, 1080, 1500), (360, 360)),
             'cover-feed-3x4.png': ((0, 240, 1080, 1680), (360, 480))}
    crop_records = []
    for filename, (box, size) in crops.items():
        assert thumb['headline_bounds'][0] >= box[0] and thumb['headline_bounds'][1] >= box[1]
        assert thumb['headline_bounds'][2] <= box[2] and thumb['headline_bounds'][3] <= box[3]
        cover.crop(box).resize(size, Image.Resampling.LANCZOS).save(qa / filename)
        crop_records.append({'image': filename, 'source_crop': list(box), 'preview_size': list(size),
                             'entire_headline_inside_crop': True})
    required_files = ['opening-0.0s.png', 'opening-0.5s.png', 'opening-1.0s.png', 'opening-2.0s.png',
                      'cover-feed-9x16.png', 'cover-grid-square.png', 'cover-feed-3x4.png', 'mobile-preview.png']
    result = {'required_files': ['qa/' + name for name in required_files], 'source_frame0_cover_exact': True,
              'first_frame': first_metrics, 'headline_stable_through_one_second': True,
              'headline_samples': 61, 'headline_roi': list(headline_roi),
              'technical_roi': list(technical_roi), 'technical_first_motion_s': first_change,
              'technical_unique_frames_first_second': len(set(hashes)),
              'maximum_changed_technical_pixels_first_second': max(changes),
              'transition_samples': transition,
              'transition_maximum_mean_rgb_delta': max(r['mean_absolute_rgb_delta'] for r in transition),
              'encoded_snapshots': actuals, 'crop_previews': crop_records,
              'caption_checks': caption_record, 'thumbnail_settings': thumb, 'subtitle_settings': sub,
              'review_scope': 'Actual decoded opening images and source style/layout correspondence. Preview crops model likely feed/grid crops; no automatic platform selection, physical-phone playback or perceptual listening approval is claimed.'}
    (qa / 'qa-summary.json').write_text(json.dumps(result, indent=2) + '\n')
    (evidence / 'final-opening-validation.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
