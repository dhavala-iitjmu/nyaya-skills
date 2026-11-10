import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('judge',ROOT/'ke/vada-samvada/scripts/judge.py')
judge=importlib.util.module_from_spec(spec);spec.loader.exec_module(judge)

class DialogicalSkills(unittest.TestCase):
    def fixture(self):
        return {'criteria':[{'id':'identity','mandatory':True},{'id':'coverage','weight':2}],
          'assessments':[{'id':'identity','status':'pass','reason':'Exact accepted identifier','evidence':['entity:1']},
                         {'id':'coverage','status':'pass','score':90,'reason':'Approved examples covered','evidence':['test:1']}], 'remaining_turns':2}
    def test_quality_never_overrides_failed_gate(self):
        body=self.fixture();self.assertEqual(judge.evaluate(body)['decision'],'graduate')
        body['assessments'][0]['status']='fail'
        self.assertEqual(judge.evaluate(body)['decision'],'revise')
    def test_unknown_evidence_and_exhaustion(self):
        body=self.fixture();body['assessments'][0]['evidence']=[]
        self.assertEqual(judge.evaluate(body)['decision'],'clarify')
        body['remaining_turns']=0;self.assertEqual(judge.evaluate(body)['decision'],'escalate')
    def test_missing_or_invalid_scores_are_not_success(self):
        body=self.fixture();body['assessments'].pop()
        self.assertFalse(judge.evaluate(body)['accepted'])
        body=self.fixture();body['assessments'][1]['score']=float('nan')
        with self.assertRaises(ValueError):judge.evaluate(body)
    def test_catalog_entries_are_self_contained_skills(self):
        body=json.loads((ROOT/'catalog.json').read_text());self.assertEqual(len(body['skills']),10)
        for entry in body['skills']:
            text=(ROOT/entry['path']/'SKILL.md').read_text()
            self.assertTrue(text.startswith('---\nname: '+entry['name']+'\n'))
            self.assertEqual(entry['category'],entry['path'].split('/')[0])
            self.assertTrue((ROOT/entry['path']/'examples').is_dir())
            if entry['category']=='ke':
                for section in ('Inputs and applicability','Method','Acceptance rubric','Feedback, stopping and authority'):self.assertIn(section,text)
            self.assertNotIn('../../',text)

    def test_category_indexes_and_skill_example_links_resolve(self):
        import re
        for path in ROOT.rglob('*.md'):
            if '.git' in path.parts or '.venv' in path.parts:continue
            for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if target.startswith(('http://','https://','#')):continue
                self.assertTrue((path.parent/target).is_file(),str(path)+': '+target)
        self.assertFalse((ROOT/'skills').exists());self.assertFalse((ROOT/'examples').exists())
