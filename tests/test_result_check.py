import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'research/research-result-check/scripts/summarize_results.py'
spec = importlib.util.spec_from_file_location('result_check', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def data(baseline=(1, 3), candidate=(2, 6), direction='higher'):
    return {'metric': 'score', 'direction': direction,
            'runs': [{'seed': i, 'baseline': b, 'candidate': c}
                     for i, (b, c) in enumerate(zip(baseline, candidate))]}


class ResultCheck(unittest.TestCase):
    def test_known_paired_statistics_and_units(self):
        result = module.summarize(data())
        self.assertEqual(result['baseline']['mean'], 2)
        self.assertEqual(result['candidate']['mean'], 4)
        self.assertEqual(result['signed_improvement']['mean'], 2)
        self.assertAlmostEqual(result['signed_improvement']['sample_std'], math.sqrt(2))
        self.assertEqual(result['relative_improvement_percent'], 100)
        self.assertEqual(result['improved_runs'], 2)
        self.assertEqual(result['claim_status'], 'descriptive_only')

    def test_lower_is_better_and_mixed_outcomes(self):
        result = module.summarize(data((100, 100, 100), (90, 100, 110), 'lower'))
        self.assertEqual(result['signed_improvement']['mean'], 0)
        self.assertEqual([result[k] for k in ('improved_runs', 'tied_runs', 'worse_runs')], [1, 1, 1])
        result = module.summarize(data((100, 120, 80), (90, 110, 70), 'lower'))
        self.assertEqual(result['relative_improvement_percent'], 10)

    def test_single_run_and_zero_baseline(self):
        result = module.summarize(data((0,), (2,)))
        self.assertIsNone(result['baseline']['sample_std'])
        self.assertIsNone(result['signed_improvement']['sample_std'])
        self.assertIsNone(result['relative_improvement_percent'])
        self.assertEqual(result['signed_improvement']['mean'], 2)

    def test_rejects_ambiguous_or_invalid_measurements(self):
        for value in (True, float('nan'), float('inf'), '2', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.summarize(data((value,), (2,)))
        for invalid in ({}, {'metric': 'score', 'direction': 'guess', 'runs': []}, []):
            with self.assertRaises(ValueError):
                module.summarize(invalid)
        duplicate = data()
        duplicate['runs'][1]['seed'] = '0'
        with self.assertRaisesRegex(ValueError, 'Duplicate seed'):
            module.summarize(duplicate)

    def test_cli_produces_summary_without_mutating_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'results.json'
            source.write_text(json.dumps(data()))
            original = source.read_bytes()
            output = Path(tmp) / 'summary.json'
            result = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text())['paired_runs'], 2)
            self.assertEqual(source.read_bytes(), original)
            blocked = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source), '--output', str(source)], capture_output=True, text=True)
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(source.read_bytes(), original)

    def test_cli_invalid_input_creates_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'invalid.json';source.write_text('{"metric": "score"}')
            output = Path(tmp) / 'summary.json'
            result = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('direction', result.stderr)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
