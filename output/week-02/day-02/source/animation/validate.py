#!/usr/bin/env python3
"""Validate the actual dependency-resolution export, cover opening and styled captions.
No publication, playback listening or subjective voice acceptance is implied.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import struct

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'source/evidence'
V = ROOT / 'video.mp4'
E.mkdir(parents=True, exist_ok=True)


def run(cmd, stem, raw=False):
    result = subprocess.run(cmd, capture_output=True, text=not raw)
    (E / f'final-{stem}.command.json').write_text(json.dumps(
        {'command': cmd, 'exit_code': result.returncode}, indent=2) + '\n')
    stderr = result.stderr.decode(errors='replace') if raw else result.stderr
    (E / f'final-{stem}.stderr.txt').write_text(stderr)
    if not raw:
        (E / f'final-{stem}.stdout.txt').write_text(result.stdout)
    if result.returncode:
        raise RuntimeError((stem, result.returncode, stderr))
    return result


def parse_ssim(path):
    return [float(re.search(r'All:([0-9.]+)', line).group(1))
            for line in path.read_text().splitlines()]


def words(text):
    # Java method/class spelling may be displayed without its spoken spaces.
    text = text.lower().replace('’', "'").replace("'", '')
    text = text.replace('get bean', 'getbean').replace('application context', 'applicationcontext')
    text = text.replace('@bean', 'bean').replace('@component', 'component')
    return re.findall(r'[a-z0-9]+', text)


def srt_seconds(text):
    h, m, tail = text.split(':')
    s, ms = tail.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def verify_fast_start(path):
    """Inspect actual top-level MP4 atoms without assuming FFmpeg options worked."""
    atoms = []
    size = path.stat().st_size
    with path.open('rb') as stream:
        position = 0
        while position < size:
            stream.seek(position)
            header = stream.read(8)
            assert len(header) == 8, ('Truncated MP4 atom header', position)
            length, kind = struct.unpack('>I4s', header)
            header_size = 8
            if length == 1:
                extended = stream.read(8)
                assert len(extended) == 8
                length = struct.unpack('>Q', extended)[0]
                header_size = 16
            elif length == 0:
                length = size - position
            assert length >= header_size and position + length <= size, ('Invalid MP4 atom size', position, length)
            atoms.append({'type': kind.decode('ascii', errors='replace'), 'offset': position, 'bytes': length})
            position += length
    moov = next(a['offset'] for a in atoms if a['type'] == 'moov')
    mdat = next(a['offset'] for a in atoms if a['type'] == 'mdat')
    assert moov < mdat, 'MP4 metadata is after media data; fast-start requirement failed'
    return {'top_level_atoms': atoms, 'moov_before_mdat': True, 'moov_offset': moov, 'first_mdat_offset': mdat}


def source_audio_metrics():
    result = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i',
                  str(ROOT / 'narration.wav'), '-f', 'f32le', '-ac', '1',
                  '-ar', '48000', 'pipe:1'], 'narration-signal', raw=True)
    signal = np.frombuffer(result.stdout, dtype='<f4')
    assert len(signal) > 2 * 48000
    active = np.flatnonzero(np.abs(signal) > 10 ** (-60 / 20))
    assert len(active)
    onset = int(active[0]) / 48000
    assert onset < .15, ('Narration does not begin immediately', onset)
    rms = float(20 * np.log10(max(1e-12, float(np.sqrt(np.mean(signal[:96000] ** 2))))))
    assert rms > -40, ('Hook speech energy is unexpectedly low', rms)
    return {'source_narration_onset_s': onset,
            'source_first_two_seconds_rms_dbfs': rms,
            'source_narration_duration_s': len(signal) / 48000}


def main():
    fast_start = verify_fast_start(V)
    (E / 'final-fast-start.json').write_text(json.dumps(fast_start, indent=2) + '\n')
    p = run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams',
             '-show_format', '-of', 'json', str(V)], 'ffprobe')
    probe = json.loads(p.stdout)
    (E / 'final-ffprobe.json').write_text(json.dumps(probe, indent=2) + '\n')
    v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    a = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    assert (v['codec_name'], v['width'], v['height'], v['pix_fmt']) == ('h264', 1080, 1920, 'yuv420p')
    assert v['r_frame_rate'] == v['avg_frame_rate'] == '60/1'
    assert v.get('field_order') == 'progressive' and v.get('bits_per_raw_sample') == '8'
    assert abs(float(v['start_time'])) < .001 and abs(float(a['start_time'])) < .001
    assert all(v[k] == 'bt709' for k in ['color_space', 'color_transfer', 'color_primaries'])
    assert v['color_range'] == 'tv'
    assert (a['codec_name'], a['sample_rate'], a['channels']) == ('aac', '48000', 2)
    duration = float(probe['format']['duration'])
    assert 0 < duration < 45, ('Duration must be positive and strictly below 45 seconds', duration)
    run(['ffmpeg', '-v', 'error', '-i', str(V), '-f', 'null', '-'], 'decode')
    run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(V), '-af',
         'loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json', '-f', 'null', '-'], 'audio-loudness')
    run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(V), '-af',
         'silencedetect=noise=-50dB:d=0.15', '-f', 'null', '-'], 'audio-silence')
    run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(V), '-vf',
         'blackdetect=d=0.01:pix_th=0.015:pic_th=0.99', '-an', '-f', 'null', '-'], 'black-detect')

    f = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
             'frame=best_effort_timestamp_time', '-of', 'json', str(V)], 'frame-timestamps')
    timestamps = [float(x['best_effort_timestamp_time']) for x in json.loads(f.stdout)['frames']]
    assert len(timestamps) == int(v['nb_read_frames'])
    assert abs(timestamps[0]) < .001
    assert all(abs(y - x - 1 / 60) < 2e-6 for x, y in zip(timestamps, timestamps[1:]))

    spec = importlib.util.spec_from_file_location('render', ROOT / 'source/animation/render.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    data = renderer.read_timing()
    assert int(v['nb_read_frames']) == math.ceil(data['duration'] * 60)
    assert abs(duration - int(v['nb_read_frames']) / 60) < .000002
    assert Image.open(ROOT / 'cover.png').size == (1080, 1920)
    mechanism_crop = (100, 330, 980, 1290)
    opening_spec = importlib.util.spec_from_file_location('opening_qa', ROOT / 'source/animation/opening_qa.py')
    opening_module = importlib.util.module_from_spec(opening_spec)
    opening_spec.loader.exec_module(opening_module)
    opening_record = opening_module.validate_opening(ROOT, renderer, data, run, parse_ssim)
    opening_results = opening_record['encoded_snapshots']
    first_change = opening_record['technical_first_motion_s']

    audio_metrics = source_audio_metrics()
    assert abs(float(a['duration']) - audio_metrics['source_narration_duration_s']) < .03
    encoded_audio = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(V), '-t', '2',
                         '-f', 'f32le', '-ac', '1', '-ar', '48000', 'pipe:1'], 'opening-audio', raw=True)
    pcm = np.frombuffer(encoded_audio.stdout, dtype='<f4')
    assert len(pcm) >= 95000
    audio_metrics['encoded_first_two_seconds_rms_dbfs'] = float(20 * np.log10(
        max(1e-12, float(np.sqrt(np.mean(pcm ** 2))))))
    assert audio_metrics['encoded_first_two_seconds_rms_dbfs'] > -40
    (E / 'final-opening-audio-metrics.json').write_text(json.dumps(audio_metrics, indent=2) + '\n')

    samples = sorted(set([n / 60 for n in range(120)] +
                         [s['start'] + (s['end'] - s['start']) * j / 16
                          for s in data['scenes'] for j in range(17)
                          if s['start'] + (s['end'] - s['start']) * j / 16 < data['duration']] +
                         [(c['start'] + c['end']) / 2 for c in data['captions']]))
    bounds = []
    for t in samples:
        image = np.asarray(renderer.render_frame(t, data))
        ys, xs = np.where(image.max(axis=2) >= 90)
        box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        assert box[0] >= 90 and box[1] >= 250 and box[2] <= 990 and box[3] <= 1520, (t, box)
        bounds.append({'time': t, 'bright_content_bounds': box})
    (E / 'final-source-safe-bounds.json').write_text(json.dumps(bounds, indent=2) + '\n')

    blocks = (ROOT / 'subtitles.srt').read_text().strip().split('\n\n')
    previous_end = 0
    texts = []
    for i, block in enumerate(blocks, 1):
        lines = block.splitlines()
        assert int(lines[0]) == i and 1 <= len(lines[2:]) <= 2
        start, end = map(srt_seconds, lines[1].split(' --> '))
        assert previous_end <= start < end <= duration
        previous_end = end
        expected = data['captions'][i - 1]
        assert abs(start - expected['start']) < .00051 and abs(end - expected['end']) < .00051
        displayed = ' '.join(lines[2:])
        assert words(displayed) == words(expected['text']), (displayed, expected['text'])
        texts.append(displayed)
    assert len(blocks) == len(data['captions'])
    phrases = data.get('phrases', data['captions'])
    assert phrases[0]['start'] == 0 and phrases[0]['text'] == 'How does Spring know what to inject?'
    assert phrases[0]['end'] > 0, 'Actual spoken hook duration must be retained'
    assert words(' '.join(texts)) == words(' '.join(p['text'] for p in phrases))
    asr = json.loads((ROOT / 'source/voice/asr-summary.json').read_text())
    narration_hash = hashlib.sha256((ROOT / 'narration.wav').read_bytes()).hexdigest()
    assert asr['narration_sha256'] == narration_hash, 'ASR belongs to a different narration file'
    assert asr['reference_words'] == len(words(' '.join(p['text'] for p in phrases)))
    assert abs(asr['normalized_word_error_rate'] - asr['edit_distance'] / asr['reference_words']) < 1e-12
    assert asr.get('model'), 'Actual speech recognition model must be identified'
    assert data['captions'][0]['start'] <= .15
    assert len(data['scenes']) == 7
    assert data['scenes'][-2]['scene'] == 6 and data['scenes'][-1]['scene'] == 7
    assert words(phrases[-1]['text']) == words(texts[-1]) == ['thanks', 'for', 'watching']

    hold_seconds = float(data['recap_hold_seconds'])
    hold_start = float(data['recap_hold_start'])
    hold_end = float(data['recap_hold_end'])
    recap_scene, thanks_scene = data['scenes'][-2:]
    assert hold_seconds >= 2
    assert abs(hold_end - hold_start - hold_seconds) < .000002
    assert recap_scene['start'] <= hold_start < hold_end <= recap_scene['end'] + .000001
    assert abs(thanks_scene['start'] - hold_end) < .000002
    assert abs(float(data['thanks_start']) - thanks_scene['start']) < .000002
    assert abs(float(data['thanks_end']) - thanks_scene['end']) < .000002
    hold_first = math.ceil(hold_start * 60 - 1e-7)
    hold_samples = [hold_first / 60 + n / 60 for n in range(120)]
    assert hold_samples[0] >= hold_start - 1e-6 and hold_samples[-1] < hold_end + .000001
    recap_crop = tuple(data.get('recap_hold_crop', mechanism_crop))
    assert len(recap_crop) == 4
    assert recap_crop[0] >= 90 and recap_crop[1] >= 250 and recap_crop[2] <= 990 and recap_crop[3] < 1322
    w, h = recap_crop[2] - recap_crop[0], recap_crop[3] - recap_crop[1]
    assert w % 2 == h % 2 == recap_crop[0] % 2 == recap_crop[1] % 2 == 0
    crop_filter = f'crop={w}:{h}:{recap_crop[0]}:{recap_crop[1]}'
    reference = renderer.render_frame(hold_end - .03, data).crop(recap_crop)
    reference_array = np.asarray(reference)
    assert all(np.array_equal(np.asarray(renderer.render_frame(t, data).crop(recap_crop)), reference_array)
               for t in hold_samples), 'The complete recap changes during its reading hold'
    reference.save(E / 'final-recap-hold-reference.png')
    run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(V), '-loop', '1', '-framerate', '60', '-i',
         str(E / 'final-recap-hold-reference.png'), '-filter_complex',
         f'[0:v]trim=start_frame={hold_first},setpts=PTS-STARTPTS,{crop_filter}[recap];'
         '[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[reference];'
         f'[recap][reference]ssim=stats_file={E}/final-recap-hold-ssim-frames.txt',
         '-frames:v', '120', '-an', '-f', 'null', '-'], 'recap-hold-ssim')
    hold_ssims = parse_ssim(E / 'final-recap-hold-ssim-frames.txt')
    assert len(hold_ssims) == 120 and min(hold_ssims) > .995

    thanks_frame = int(v['nb_read_frames']) - 1
    thanks_t = thanks_frame / 60
    assert thanks_t >= thanks_scene['start']
    renderer.render_frame(thanks_t, data).crop(recap_crop).save(E / 'final-thanks-reference.png')
    run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(V), '-loop', '1', '-framerate', '60', '-i',
         str(E / 'final-thanks-reference.png'), '-filter_complex',
         f'[0:v]trim=start_frame={thanks_frame},setpts=PTS-STARTPTS,{crop_filter}[ending];'
         '[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[reference];'
         f'[ending][reference]ssim=stats_file={E}/final-thanks-ssim-frames.txt',
         '-frames:v', '1', '-an', '-f', 'null', '-'], 'thanks-ssim')
    thanks_ssims = parse_ssim(E / 'final-thanks-ssim-frames.txt')
    assert len(thanks_ssims) == 1 and thanks_ssims[0] > .995

    thumbs = []
    for i, s in enumerate(data['scenes']):
        t = s['start'] + .8 * (s['end'] - s['start'])
        destination = E / f'final-decoded-scene-{i + 1}.png'
        run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(t),
             '-i', str(V), '-frames:v', '1', str(destination)], f'decoded-scene-{i + 1}')
        thumbs.append(Image.open(destination).resize((360, 640), Image.Resampling.LANCZOS))
    contact = Image.new('RGB', (1080, math.ceil(len(thumbs) / 3) * 640), '#080f20')
    for i, image in enumerate(thumbs):
        contact.paste(image, (i % 3 * 360, i // 3 * 640))
    contact.save(E / 'final-decoded-mobile-contact.png')

    # Preserve actual before/after cut frames for the production agent to review.
    # These are inspection evidence, not a claim of a human playback review.
    transition_contact = Image.new('RGB', (720, 640 * (len(data['scenes']) - 1)), '#080f20')
    transitions = []
    for i, s in enumerate(data['scenes'][1:], 1):
        pair = []
        for j, offset in enumerate([-.05, .05]):
            t = max(0, s['start'] + offset)
            destination = E / f'final-transition-{i}-{j}.png'
            run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(t),
                 '-i', str(V), '-frames:v', '1', str(destination)], f'transition-{i}-{j}')
            transition_contact.paste(Image.open(destination).resize((360, 640), Image.Resampling.LANCZOS),
                                     (j * 360, (i - 1) * 640))
            pair.append({'requested_time_s': t, 'image': destination.name})
        transitions.append({'scene_start_s': s['start'], 'before_after': pair})
    transition_contact.save(E / 'final-decoded-transition-contact.png')
    (E / 'final-transition-samples.json').write_text(json.dumps(transitions, indent=2) + '\n')

    assert hasattr(renderer, 'mechanism_anchors'), 'Renderer must expose dependency-resolution anchors'
    anchors = {key: float(value) for key, value in renderer.mechanism_anchors(data).items()}
    ordered = ['required_type_s', 'dependency_descriptor_s', 'compatible_candidates_s',
               'unrelated_excluded_s', 'eligibility_filter_s', 'selected_candidate_s',
               'constructor_supplied_s', 'reference_stored_s', 'no_eligible_candidate_s',
               'startup_failure_s', 'verification_s', 'selection_scope_s', 'recap_match_s',
               'recap_filter_s', 'recap_inject_s', 'recap_complete_s']
    assert set(ordered).issubset(anchors), ('Missing resolution anchors', sorted(set(ordered) - set(anchors)))
    assert all(anchors[left] < anchors[right] for left, right in zip(ordered, ordered[1:])), anchors
    assert all(0 <= t < duration for t in anchors.values())
    assert anchors['recap_complete_s'] <= hold_start + .000002
    graph_ready_s = float(renderer.graph_ready_at(data))
    application_use_start_s = float(renderer.application_use_start(data))
    assert abs(graph_ready_s - anchors['reference_stored_s']) < .000002
    assert abs(application_use_start_s - graph_ready_s) < .000002

    # Independently captured real JUnit executions verify the illustrated path.
    # Two refresh warnings are expected because negative contexts are tested.
    java = json.loads((E / 'java-verification-result.json').read_text())
    assert all(java[key] == 0 for key in ['compile_main_exit_code', 'compile_tests_exit_code', 'junit_exit_code'])
    assert java['tests_found'] == java['tests_succeeded'] == 3 and java['tests_failed'] == java['tests_skipped'] == 0
    assert java['compile_stderr_empty'] is True and java['junit_stderr_empty'] is False
    assert java['expected_negative_context_warnings'] is True
    assert java['spring_framework_version'] == '6.2.11'
    for relative, expected in java['source_sha256'].items():
        assert hashlib.sha256((ROOT / 'source/java' / relative).read_bytes()).hexdigest() == expected, relative
    expected_proofs = {'compatible candidates: 2', 'eligible candidates: 1', 'unrelated ignored: true',
                       'gateway same: true', 'disabled candidate missing: true', 'disabled compatible candidates: 1',
                       'disabled eligible candidates: 0', 'missing candidate: true',
                       'missing exception: NoSuchBeanDefinitionException',
                       'missing startup exception: UnsatisfiedDependencyException'}
    assert expected_proofs == set(java['test_stdout_proof_lines']) == set(java['proof_lines'])
    semantics = java['verified_semantics']
    semantic_keys = {'compatible_type_candidates_discovered', 'unrelated_named_bean_ignored_for_required_type',
                     'autowire_disabled_candidate_filtered', 'one_eligible_gateway_injected_by_reference',
                     'missing_required_candidate_fails_startup', 'matching_disabled_bean_is_not_eligible'}
    assert all(semantics.get(key) is True for key in semantic_keys), semantics
    assert semantics.get('real_payment_performed') is False
    raw_junit_lines = set((E / 'java-junit.stdout.txt').read_text().splitlines())
    assert expected_proofs.issubset(raw_junit_lines)
    junit_stderr = (E / 'java-junit.stderr.txt').read_text()
    assert junit_stderr.count('WARNING: Exception encountered during context initialization') == 2
    assert junit_stderr.count('UnsatisfiedDependencyException') == 2
    assert junit_stderr.count('No qualifying bean of type') == 2
    trace = json.loads((E / java['runtime_trace_file']).read_text())
    expected_events = ['resolveDependency: PaymentGateway',
                       'compatible types: [eligibleGateway, backupGateway]',
                       'isAutowireCandidate eligibleGateway: true',
                       'isAutowireCandidate backupGateway: false',
                       'eligible candidates: [eligibleGateway]']
    assert trace['spring_framework_version'] == '6.2.11' and trace['events'] == expected_events
    implementation = json.loads((E / 'java-implementation-sources.json').read_text())
    assert implementation['version'] == '6.2.11' and implementation['http_status'] == 200
    assert implementation['published_sha1_http_status'] == 200
    for name, expected in implementation['extracted_files'].items():
        path = ROOT / 'source/java/framework' / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    source_jar = ROOT / 'source/java/framework/spring-beans-6.2.11-sources.jar'
    assert hashlib.sha256(source_jar.read_bytes()).hexdigest() == implementation['source_jar_sha256']
    inspection = json.loads((E / 'java-implementation-inspection.json').read_text())
    assert inspection['spring_version'] == '6.2.11'
    assert inspection['source_jar_sha256'] == implementation['source_jar_sha256']
    inspected_ids = set()
    for excerpt in inspection['excerpts']:
        path = (E / excerpt['file']).resolve()
        assert path.is_relative_to((ROOT / 'source/java/framework').resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == excerpt['source_file_sha256']
        lines = path.read_text().splitlines()
        observed = '\n'.join(lines[excerpt['line_start'] - 1:excerpt['line_end']])
        assert observed.rstrip('\n') == excerpt['excerpt'].rstrip('\n'), excerpt['id']
        inspected_ids.add(excerpt['id'])
    assert {'resolve-entry', 'shortcut-and-value', 'name-shortcut', 'type-discovery-and-eligibility',
            'single-candidate-selection', 'candidate-definition-flag', 'multiple-candidate-selection-policy'}.issubset(inspected_ids)
    official_docs = json.loads((E / 'java-doc-official-documentation.json').read_text())
    docs_by_slug = {page['slug']: page for page in official_docs}
    for page in official_docs:
        assert page['http_status'] == 200
        assert hashlib.sha256((E / page['html_file']).read_bytes()).hexdigest() == page['sha256']
        assert hashlib.sha256((E / page['text_file']).read_bytes()).hexdigest() == page['text_sha256']
    doc_claims = json.loads((E / 'java-doc-claim-verification.json').read_text())
    for claim in doc_claims['claims']:
        page = docs_by_slug[claim['page']]
        assert claim['source_html_sha256'] == page['sha256']
        text = (E / page['text_file']).read_text()
        assert text[claim['text_offset']:claim['text_offset'] + len(claim['exact_excerpt'])] == claim['exact_excerpt']
    policy_records = json.loads((E / 'policy-official-snapshots.json').read_text())
    for policy in policy_records:
        assert policy['http_status'] == 200
        retained = (E / f"policy-{policy['slug']}.txt").read_text()
        assert policy['response_sha256'] in retained and policy['requested_url'] in retained
        assert policy['exact_excerpt'] and policy['exact_excerpt'] in retained
    provenance = {'framework_source_jar_sha256': implementation['source_jar_sha256'],
                  'framework_source_hashes_checked': implementation['extracted_files'],
                  'framework_verbatim_excerpts_checked': len(inspection['excerpts']),
                  'official_spring_pages_hash_checked': len(official_docs),
                  'official_spring_claims_verbatim_checked': len(doc_claims['claims']),
                  'policy_retained_excerpt_records_consistent': len(policy_records),
                  'policy_check_scope': 'Fetched metadata and short retained excerpts are internally consistent. '
                                        'Full policy responses were not retained; response hashes are fetch-time evidence, '
                                        'not recomputed here. No platform approval is implied.'}
    (E / 'final-provenance-validation.json').write_text(json.dumps(provenance, indent=2) + '\n')
    causal = {'anchors': anchors, 'required_type_before_compatible_discovery': True,
              'compatible_candidates_before_eligibility_filter': True,
              'one_eligible_candidate_before_constructor_supply': True,
              'constructor_supply_before_stored_reference': True,
              'missing_eligible_candidate_before_startup_failure': True,
              'ready_service_reference_marked_without_business_execution': True,
              'real_payment_performed': False,
              'java_tests_found': java['tests_found'], 'java_tests_succeeded': java['tests_succeeded'],
              'java_current_sources_match_tested_hashes': True,
              'java_raw_junit_stdout_matches_proofs': True,
              'actual_java_proof_lines': sorted(expected_proofs), 'actual_runtime_trace': trace,
              'java_verified_semantics': {key: semantics[key] for key in sorted(semantic_keys | {'real_payment_performed'})},
              'framework_version': implementation['version'],
              'framework_source_hashes_checked': implementation['extracted_files'],
              'source_inspection_and_documentation_provenance': provenance,
              'basis': 'Animated edit anchors establish explanatory ordering, not measured Spring/JUnit wall-clock performance. '
                       'Three recorded actual JUnit/Spring context tests independently verify two compatible types, '
                       'one eligible candidate, unrelated same-named bean exclusion, exact constructor reference '
                       'and two required-candidate startup failures. The actual observer delegates all selection decisions '
                       'to Spring. The simplified sequence is specific to this dependency; Spring6.2.11 also has shortcut '
                       'and name-related paths, and qualifier/primary rules can affect selection. '
                       'No standalone app main, business execution, real payment, comprehensive application test, '
                       'universal type-first sequence or resolution performance is claimed. '
                       'This media validator checks recorded execution/source evidence without rerunning Java.'}
    (E / 'final-resolution-order.json').write_text(json.dumps(causal, indent=2) + '\n')
    for label, t in anchors.items():
        run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(t + .05), '-i', str(V),
             '-frames:v', '1', str(E / f'final-anchor-{label}.png')], f'anchor-{label}')

    # Inspect bright-content margins in actual decoded full-size stills as well
    # as source samples. This is a sampled bounds check, not all-frame readability.
    last_decoded = E / 'final-decoded-thanks-last.png'
    run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(thanks_t),
         '-i', str(V), '-frames:v', '1', str(last_decoded)], 'decoded-thanks-last')
    decoded_images = sorted(set(E.glob('final-opening-decoded-*.png')) |
                            set(E.glob('final-decoded-scene-*.png')) |
                            set(E.glob('final-transition-*-*.png')) |
                            set(E.glob('final-anchor-*.png')) | {last_decoded})
    decoded_bounds = []
    for path in decoded_images:
        with Image.open(path) as image:
            assert image.size == (1080, 1920), path.name
            array = np.asarray(image.convert('RGB'))
        ys, xs = np.where(array.max(axis=2) >= 90)
        box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        assert box[0] >= 90 and box[1] >= 250 and box[2] <= 990 and box[3] <= 1520, (path.name, box)
        decoded_bounds.append({'image': path.name, 'bright_content_bounds': box})
    (E / 'final-decoded-safe-bounds.json').write_text(json.dumps(decoded_bounds, indent=2) + '\n')

    loud = (E / 'final-audio-loudness.stderr.txt').read_text()
    metrics = json.JSONDecoder().raw_decode(loud[loud.rfind('{'):])[0]
    black_count = len(re.findall('black_start:', (E / 'final-black-detect.stderr.txt').read_text()))
    assert not (E / 'final-decode.stderr.txt').read_text().strip() and black_count == 0
    assert float(metrics['input_tp']) < 0 and -18 < float(metrics['input_i']) < -14
    silence_log = (E / 'final-audio-silence.stderr.txt').read_text()
    silence_pairs = re.findall(r'silence_start: ([0-9.]+).*?silence_end: ([0-9.]+)', silence_log, re.S)
    closing_quiet_after = max(thanks_scene['start'], float(phrases[-1]['end']) - .5)
    for start, end in silence_pairs:
        start, end = float(start), float(end)
        assert (hold_start - .05 <= start < end <= hold_end + .05) or start >= closing_quiet_after, (
            'Unexpected internal silence outside reading hold or closing tail', start, end)
    video_hash = hashlib.sha256(V.read_bytes()).hexdigest()
    (E / 'final-video.sha256').write_text(video_hash + '  video.mp4\n')
    validated_names = ['video.mp4', 'cover.png', 'first-frame.png', 'thumbnail-style.json',
                       'subtitle-style.json', 'subtitles.srt', 'narration.wav',
                       'source/timing.json', 'source/script-input.json',
                       'source/animation/render.py', 'source/animation/validate.py',
                       'source/animation/opening_qa.py', 'source/animation/audio_mix.py',
                       'source/animation/mix.wav', 'source/voice/asr-summary.json',
                       'source/voice/asr.json', 'source/voice/alignment-normalization.json',
                       'source/evidence/java-verification-result.json',
                       'source/evidence/java-runtime-trace.json', 'source/evidence/java-junit.stdout.txt',
                       'source/evidence/java-junit.stderr.txt', 'source/evidence/java-implementation-sources.json',
                       'source/evidence/java-implementation-inspection.json',
                       'source/evidence/java-doc-official-documentation.json',
                       'source/evidence/java-doc-claim-verification.json',
                       'source/evidence/policy-official-snapshots.json']
    validated_hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in validated_names}
    summary = {'video_sha256': video_hash, 'validated_file_sha256': validated_hashes, 'duration': duration, 'video_duration': float(v['duration']),
               'audio_duration': float(a['duration']), 'frames': int(v['nb_read_frames']),
               'timestamps_checked': len(timestamps), 'fps': v['r_frame_rate'],
               'video_codec': v['codec_name'], 'audio_codec': a['codec_name'], 'pixel_format': v['pix_fmt'], 'fast_start': fast_start,
               'color_space': v['color_space'], 'color_transfer': v['color_transfer'], 'color_primaries': v['color_primaries'],
               'audio_sample_rate': a['sample_rate'], 'audio_channels': a['channels'], 'srt_cues': len(blocks),
               'source_safe_bounds_samples': len(samples), 'decoded_safe_bounds_samples': len(decoded_bounds),
               'decoded_safe_bounds_sampled_only': True, 'caption_words_match_script': True,
               'scenes_count': len(data['scenes']), 'target_duration_35_40_pass': 35 <= duration <= 40,
               'caption_max_characters': max(len(c['text']) for c in data['captions']),
               'opening_static_cover_hold': False,
               'opening_source_unique_core_frames': opening_record['technical_unique_frames_first_second'],
               'opening_thumbnail_composition_preserved_first_second': True,
               'source_frame0_exact_cover': opening_record['source_frame0_cover_exact'],
               'opening_headline_stable_through_one_second': True,
               'opening_first_visual_change_s': first_change, 'opening_frame0_source_ssim': opening_results[0]['source_ssim'],
               'opening_ssim_minimum': min(x['source_ssim'] for x in opening_results),
               'opening_encoded_snapshots_compared': len(opening_results),
               'decoded_transition_pairs_retained': len(transitions),
               'source_narration_onset_s': audio_metrics['source_narration_onset_s'],
               'source_spoken_hook_end_s': phrases[0]['end'],
               'spoken_hook_complete_within_two_seconds': phrases[0]['end'] <= 2,
               'hook_completion_within_two_seconds_is_not_required_by_current_brief': True,
               'asr_model': asr['model'], 'asr_reference_words': asr['reference_words'],
               'asr_recognized_words': asr['asr_words'], 'asr_edit_distance': asr['edit_distance'],
               'asr_normalized_word_error_rate': asr['normalized_word_error_rate'],
               'asr_matches_current_narration_sha256': True,
               'encoded_first_two_seconds_rms_dbfs': audio_metrics['encoded_first_two_seconds_rms_dbfs'],
               'integrated_loudness_lufs': float(metrics['input_i']), 'true_peak_dbtp': float(metrics['input_tp']),
               'loudness_range_lu': float(metrics['input_lra']), 'decode_error_log_empty': True,
               'black_intervals_detected': black_count,
               'silence_intervals': re.findall(r'silence_start: ([0-9.]+)', silence_log),
               'compatible_type_discovery_verified': True, 'eligible_candidate_filtering_verified': True,
               'unrelated_same_named_bean_excluded_verified': True, 'injected_gateway_identity_verified': True,
               'missing_and_disabled_candidate_failures_verified': True, 'framework_implementation_sources_verified': True,
               'real_payment_performed': False,
               'graph_ready_s': graph_ready_s, 'application_use_start_s': application_use_start_s,
               'graph_ready_before_application_use': None, 'application_execution_claimed': False,
               'mechanism_anchors': anchors, 'dependency_resolution_causality': causal, 'opening_qa': opening_record,
               'recap_hold_start': hold_start, 'recap_hold_end': hold_end, 'recap_hold_seconds': hold_seconds,
               'recap_hold_is_before_thanks': True, 'recap_hold_source_samples': len(hold_samples),
               'recap_hold_crop': list(recap_crop), 'recap_hold_source_pixel_identical': True,
               'recap_hold_decoded_frames': len(hold_ssims), 'recap_hold_ssim_minimum': min(hold_ssims),
               'recap_hold_ssim_average': sum(hold_ssims) / len(hold_ssims),
               'thanks_start': thanks_scene['start'], 'thanks_end': thanks_scene['end'],
               'thanks_frame_checked': thanks_frame, 'thanks_final_frame_ssim': thanks_ssims[0],
               'thanks_caption_and_script_match': True, 'intentional_recap_hold_or_closing_quiet_allowed': True,
               'perceptual_voice_review': 'UNVERIFIED: no auditory listening review performed',
               'required_delivery_files_nonempty': True}
    required_files = ['video.mp4', 'cover.png', 'first-frame.png', 'thumbnail-style.json', 'subtitles.srt',
                      'subtitle-style.json', 'narration.wav', 'narration-script.md', 'storyboard.md',
                      'youtube-metadata.md', 'facebook-metadata.md']
    assert all((ROOT / name).is_file() and (ROOT / name).stat().st_size > 0 for name in required_files)
    (E / 'final-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
