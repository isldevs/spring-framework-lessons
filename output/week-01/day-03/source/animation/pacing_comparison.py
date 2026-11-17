"""Compare actual timing records; measurements do not establish naturalness."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]


def metrics(timing, asr):
    utterance_seconds = sum(p['end'] - p['start'] for p in timing['phrases'])
    joins = sum(timing['scenes'][i]['end'] - timing['phrases'][i]['end'] for i in range(5))
    return {'narration_duration_s': timing['duration'],
            'words': asr['reference_words'],
            'utterance_seconds_including_native_pauses': utterance_seconds,
            'utterance_words_per_minute': asr['reference_words'] / utterance_seconds * 60,
            'external_normal_scene_joins_s': joins,
            'total_inserted_silence_s': timing['duration'] - utterance_seconds,
            'body_inference_speed': timing['speed'],
            'factory_scene_start_s': timing['scenes'][2]['start'],
            'request_to_failure_s': timing['scene_cues_absolute']['missing']['fail'] - timing['scene_cues_absolute']['missing']['request'],
            'factory_call_to_instance_s': timing['scene_cues_absolute']['factory']['instance'] - timing['scene_cues_absolute']['factory']['call'],
            'outside_reveal_to_missing_s': timing['scene_cues_absolute']['boundary']['miss'] - timing['scene_cues_absolute']['boundary']['outside'],
            'recap_hold_s': timing['recap_hold_seconds']}


def main():
    baseline = json.loads((ROOT / 'source/evidence/pacing-baseline.json').read_text())
    timing = json.loads((ROOT / 'source/timing.json').read_text())
    asr = json.loads((ROOT / 'source/voice/asr-summary.json').read_text())
    old = metrics(baseline['timing'], baseline['asr_summary'])
    new = metrics(timing, asr)
    assert new['body_inference_speed'] >= 1.0
    assert new['request_to_failure_s'] <= .4 and new['outside_reveal_to_missing_s'] <= .4
    assert new['recap_hold_s'] == 2
    result = {'previous_commit': baseline['commit'], 'old': old, 'new': new,
              'utterance_word_rate_increase_percent': (new['utterance_words_per_minute'] / old['utterance_words_per_minute'] - 1) * 100,
              'interpretation': 'Old speech began almost immediately; slow model pacing, stacked pauses and late visual cues created the perceived delay. New generation uses normal model pacing and earlier cues. Word-rate arithmetic and ASR are not auditory acceptance.',
              'listening_status': 'UNVERIFIED for revised voice; no auditory review performed'}
    (ROOT / 'source/evidence/pacing-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
