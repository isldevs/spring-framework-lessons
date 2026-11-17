"""Preserve an actual source-WAV silence scan; no listening claim."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    timing = json.loads((ROOT.parent / 'timing.json').read_text())
    command = ['ffmpeg', '-hide_banner', '-nostats', '-i',
               str(ROOT.parent.parent / 'narration.wav'), '-af',
               'silencedetect=noise=-45dB:d=0.12', '-f', 'null', '-']
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    (ROOT / 'silence-scan.txt').write_text(result.stderr)
    intervals = []
    for start, end in re.findall(r'silence_start: ([0-9.]+).*?silence_end: ([0-9.]+)', result.stderr, re.S):
        start, end = float(start), float(end)
        intervals.append({'start': start, 'end': end, 'duration': end - start})
    before = [v for v in intervals if v['end'] <= timing['recap_hold_start']]
    summary = {'threshold_dbfs': -45, 'minimum_duration_s': .12,
               'intervals': intervals,
               'longest_pre_recap_hold': max(before, key=lambda v: v['duration']) if before else None}
    (ROOT / 'silence-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
