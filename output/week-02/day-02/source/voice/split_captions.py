"""Phrase captions and illustrative dependency-resolution edits from actual ASR spans."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
p = ROOT.parent / 'timing.json'
d = json.loads(p.read_text())
phrases = d['phrases']
CAPTIONS = [
    ['How does Spring know what to inject?'],
    ['The order service constructor', 'requests a PaymentGateway.',
     'Spring reads that dependency.'],
    ['The bean factory finds compatible types.',
     "An unrelated logger won't match.",
     'Matching beans must also be eligible.'],
    ['Here, one eligible gateway remains.', 'Spring supplies its instance',
     'to the constructor.'],
    ['Without an eligible candidate,', 'this required constructor dependency',
     'stops context startup.'],
    ['Our tests verify both outcomes.', 'Qualifiers and primary settings',
     'can also affect selection.', 'Match, filter, inject.'],
    ['Thanks for watching.'],
]


def normalize(s):
    return re.findall(r'[a-z0-9]+', s.lower().replace('’', '').replace("'", ''))


a = json.loads((ROOT / 'asr-alignment.json').read_text())
words = [dict(w, token=t) for seg in a['segments'] for w in seg['words']
         for t in normalize(w['word'])]
transforms = a.get('script_alignment_transformations', [])
for correction in sorted(transforms, key=lambda x: x['raw_token_start'], reverse=True):
    start, end = correction['raw_token_start'], correction['raw_token_end']
    assert [w['token'] for w in words[start:end]] == correction['observed_tokens']
    first = words[start]
    words[start:end] = [{**first, 'token': token, 'start': correction['start'],
                         'end': correction['end'], 'caption_alignment_only': True}
                        for token in correction['script_tokens']]
assert normalize(' '.join(c['text'] for c in phrases)) == [w['token'] for w in words]

new = []
offset = 0
by_scene = {}
for c, rows in zip(phrases, CAPTIONS):
    tokens = normalize(c['text'])
    assert tokens == normalize(' '.join(rows))
    by_scene[c['scene']] = words[offset:offset + len(tokens)]
    for i, text in enumerate(rows):
        n = len(normalize(text))
        start = c['start'] if i == 0 else words[offset]['start']
        offset += n
        end = c['end'] if i == len(rows) - 1 else words[offset]['start']
        start, end = max(c['start'], start), min(c['end'], end)
        assert c['start'] <= start < end <= c['end'], (text, start, end)
        assert 3 <= len(text.split()) <= 7, (text, len(text.split()))
        new.append({'scene': c['scene'], 'start': round(start, 6),
                    'end': round(end, 6), 'text': text})
assert offset == len(words)
for x, y in zip(new, new[1:]):
    assert x['end'] <= y['start']
assert new[0]['text'] == phrases[0]['text']
assert new[0]['start'] == 0 and new[0]['end'] == phrases[0]['end']
d['captions'] = new
scenes = {s['scene']: s for s in d['scenes']}


def anchor(number, token, occurrence=0):
    hits = [w for w in by_scene[number] if w['token'] == token]
    assert len(hits) > occurrence, (number, token)
    return round(max(scenes[number]['start'], hits[occurrence]['start']), 6)


def word_end(number, token, occurrence=0):
    hits = [w for w in by_scene[number] if w['token'] == token]
    assert len(hits) > occurrence, (number, token)
    return round(min(scenes[number]['end'], hits[occurrence]['end']), 6)


required = {'parameter': anchor(2, 'paymentgateway'),
            'descriptor': anchor(2, 'reads')}
discovery = {'types': anchor(3, 'compatible'),
             'unrelated': anchor(3, 'unrelated'),
             'eligibility': anchor(3, 'eligible')}
selection = {'unique': anchor(4, 'one'), 'supply': anchor(4, 'supplies'),
             'stored': round(min(word_end(4, 'constructor') + .08,
                                 phrases[3]['end'] - .03), 6)}
missing = {'no_candidate': anchor(5, 'candidate'),
           'failure': anchor(5, 'stops')}
recap = {'verify': anchor(6, 'verify'), 'scope': anchor(6, 'qualifiers'),
         'match': anchor(6, 'match'), 'filter': anchor(6, 'filter'),
         'inject': anchor(6, 'inject'),
         'complete': round(min(word_end(6, 'inject') + .05,
                               d['recap_hold_start'] - .05), 6)}
d['scene_cues_absolute'] = {'required': required, 'discovery': discovery,
                            'selection': selection, 'missing': missing,
                            'recap': recap}
absolute = {**recap, 'recap_hold_start': d['recap_hold_start'],
            'recap_hold_end': d['recap_hold_end']}
d['recap_cues_absolute'] = absolute
d['recap_cues'] = {'relative_to': 'scene_start',
                   **{k: round(v - scenes[6]['start'], 6)
                      for k, v in absolute.items()}}
d['application_use_start'] = selection['stored']
d['application_use_start_semantics'] = (
    'First ready service diagram edit after supplied constructor argument; '
    'no application method invocation or runtime benchmark is claimed.')
d['opening_cover_hold'] = True
d['opening_cover_recognizable_through_s'] = 1.0
d['opening_transition_start_s'] = 1.0
d['opening_transition_end_s'] = 2.0
d['hook_text_display'] = phrases[0]['text']
d['hook_asr_last_word_end'] = word_end(1, 'inject')
d['narration_sha256'] = hashlib.sha256((ROOT.parent.parent / 'narration.wav').read_bytes()).hexdigest()
d['caption_method'] = (
    'Final sample-derived utterance/first/last-cue boundaries; intermediate '
    'unprompted small.en observed word spans. Explicit known-input caption '
    'mapping of PaymentGateway and An/and preserves raw transcript/score/times. '
    'Full hook is one exact0-to-utterance-end cue. No evenly divided timing.')
record = {
    'narration_sha256': d['narration_sha256'],
    'text_transformations': transforms,
    'raw_asr_score_unchanged': True,
    'timing_sources': 'Unprompted full-stream ASR on an approximate20ms grid; sample-derived scene/edge edits. No invented subword boundaries.',
    'first_hook_caption': new[0],
    'hook_ending_asr_s': d['hook_asr_last_word_end'],
    'derived_animation_anchors': 'selection.stored is observed constructor-end+.08s; recap.complete is inject-end+.05s. These are illustrative editing delays, not Spring runtime measurements. Raw Match zero-duration ASR token remains unchanged; its observed onset supplies a highlight anchor. Thanks ASR onset precedes its source segment and is clamped to the exact source scene start.',
    'caption_word_count_range': [min(len(c['text'].split()) for c in new),
                                 max(len(c['text'].split()) for c in new)],
    'auditory_naturalness_pronunciation_age_acceptance': 'UNVERIFIED',
}
(ROOT / 'alignment-normalization.json').write_text(json.dumps(record, indent=2) + '\n')
p.write_text(json.dumps(d, indent=2) + '\n')


def stamp(v):
    ms = round(v * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


(ROOT.parent.parent / 'subtitles.srt').write_text('\n'.join(
    f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n"
    for i, c in enumerate(new, 1)))
print(json.dumps({'captions': len(new),
                  'max_characters': max(len(c['text']) for c in new),
                  'cue_word_min': min(len(c['text'].split()) for c in new),
                  'cue_word_max': max(len(c['text'].split()) for c in new),
                  'duration': d['duration'],
                  'scene_cues_absolute': d['scene_cues_absolute'],
                  'recap_hold_start': d['recap_hold_start'],
                  'recap_hold_end': d['recap_hold_end'],
                  'hook_utterance_end': new[0]['end']}, indent=2))
