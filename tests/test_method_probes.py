import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location('probe_methods', Path(__file__).with_name('probe_methods.py'))
probe = importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)


class ProbeEvaluator(unittest.TestCase):
    def test_missing_answers_and_numeric_boolean_impersonation_fail(self):
        expected = {'known': False, 'sources': 1}
        self.assertEqual(probe.failures_for({'known': False, 'sources': 1}, expected), {})
        self.assertIn('known', probe.failures_for({'known': 0, 'sources': 1}, expected))
        self.assertIn('sources', probe.failures_for({'known': False}, expected))
        self.assertIn('sources', probe.failures_for({'known': False, 'sources': True}, expected))

    def test_bad_container_is_a_failure_not_a_success(self):
        self.assertIn('answers', probe.failures_for([], {'known': False}))
        self.assertIn('known', probe.failures_for({'known': True}, {'known': False}))


if __name__ == '__main__':unittest.main()
