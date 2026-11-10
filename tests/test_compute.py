import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('compute_experiment',ROOT/'compute/skypilot/examples/experiment.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class ComputeExperiment(unittest.TestCase):
    def source(self,root):
        p=Path(root)/'data.csv'
        with p.open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['x','y']);w.writerows((i,2*i+1) for i in range(32))
        return p

    def test_fit_uses_training_rows_and_verifies_saved_artifacts(self):
        with tempfile.TemporaryDirectory() as root:
            output=Path(root)/'output';result=module.experiment(self.source(root),output)
            self.assertEqual(result['metrics']['candidate_mae'],0)
            self.assertEqual(result['metrics']['baseline_mae'],32)
            self.assertEqual(result['metrics']['slope'],2)
            self.assertEqual(result['metrics']['train_rows'],24)
            self.assertEqual(module.verify(output),result)

    def test_modified_predictions_are_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            output=Path(root)/'output';module.experiment(self.source(root),output)
            (output/'predictions.csv').write_text('actual,prediction\n1,99\n')
            with self.assertRaises(ValueError):module.verify(output)

    def test_manifest_cannot_select_outside_files(self):
        with tempfile.TemporaryDirectory() as root:
            output=Path(root)/'output';module.experiment(self.source(root),output)
            (output/'manifest.json').write_text(json.dumps({'../data.csv':'anything'}))
            with self.assertRaises(ValueError):module.verify(output)

    def test_existing_output_is_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as root:
            output=Path(root)/'output';source=self.source(root);module.experiment(source,output)
            with self.assertRaises(ValueError):module.experiment(source,output)


if __name__=='__main__':unittest.main()
