#!/usr/bin/env python3
"""Descriptive statistics for paired experimental runs; standard library only."""
import argparse
import json
import math
from pathlib import Path
import statistics


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{label} must be a finite number')
    try:
        result = float(value)
    except OverflowError:
        raise ValueError(f'{label} must be a finite number') from None
    if not math.isfinite(result):
        raise ValueError(f'{label} must be a finite number')
    return result


def describe(values):
    return {'mean': statistics.mean(values),
            'sample_std': statistics.stdev(values) if len(values) > 1 else None}


def summarize(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    metric = data.get('metric')
    if not isinstance(metric, str) or not metric.strip():
        raise ValueError('metric must be a nonempty string including units when applicable')
    direction = data.get('direction')
    if direction not in ('higher', 'lower'):
        raise ValueError('direction must be higher or lower')
    runs = data.get('runs')
    if not isinstance(runs, list) or not runs:
        raise ValueError('runs must be a nonempty list of paired measurements')
    seeds = set()
    baseline, candidate = [], []
    for i, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ValueError(f'Run {i + 1} must be an object')
        seed = run.get('seed')
        if isinstance(seed, bool) or not isinstance(seed, (int, str)) or str(seed).strip() == '':
            raise ValueError(f'Run {i + 1} needs an integer or nonempty string seed')
        # Treat 1 and "1" as the same seed to avoid counting duplicates twice.
        key = str(seed)
        if key in seeds:
            raise ValueError(f'Duplicate seed: {seed}')
        seeds.add(key)
        baseline.append(number(run.get('baseline'), f'Run {i + 1} baseline'))
        candidate.append(number(run.get('candidate'), f'Run {i + 1} candidate'))
    sign = 1 if direction == 'higher' else -1
    improvements = [sign * (c - b) for b, c in zip(baseline, candidate)]
    if not all(math.isfinite(v) for v in improvements):
        raise ValueError('Differences exceed the supported numeric range')
    base_stats, candidate_stats = describe(baseline), describe(candidate)
    change = describe(improvements)
    relative = 100 * (change['mean'] / abs(base_stats['mean'])) if base_stats['mean'] else None
    if relative is not None and not math.isfinite(relative):
        raise ValueError('Relative improvement exceeds the supported numeric range')
    return {
        'metric': metric, 'direction': direction, 'paired_runs': len(runs),
        'baseline': base_stats, 'candidate': candidate_stats,
        'signed_improvement': change,
        'relative_improvement_percent': relative,
        'improved_runs': sum(v > 0 for v in improvements),
        'tied_runs': sum(v == 0 for v in improvements),
        'worse_runs': sum(v < 0 for v in improvements),
        'claim_status': 'descriptive_only',
        'limitations': [
            'Pairing and experimental comparability are supplied, not independently verified.',
            'No significance test or confidence interval was computed.',
            *(['Sample standard deviation is unavailable for a single paired run.'] if len(runs) == 1 else []),
            *(['Relative improvement is unavailable because the baseline mean is zero.'] if not base_stats['mean'] else []),
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.output and args.input.resolve() == args.output.resolve():
            raise ValueError('Output must not overwrite the supplied input')
        result = summarize(json.loads(args.input.read_text(encoding='utf-8')))
        text = json.dumps(result, indent=2, allow_nan=False) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding='utf-8')
        print(text, end='')
    except (ValueError, OSError, OverflowError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
