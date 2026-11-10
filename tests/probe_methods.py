"""Opt-in live behavior probes; run with Nyaya's interpreter or `nyaya run FILE`.

Tests inline SKILL.md instruction snapshots, not native skill loading/helpers.
Expected answers stay in the local evaluator and are never sent to the model.
"""
import argparse
import json
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[1]
METHODS = ('nyaya-examination', 'vaisheshika-description')


def failures_for(answers, expected):
    if not isinstance(answers, dict):return {'answers': {'error': 'Expected an object'}}
    return {key: {'expected': value, 'actual': answers.get(key)} for key, value in expected.items()
            if type(answers.get(key)) is not type(value) or answers[key] != value}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='openai/chat-latest')
    parser.add_argument('--output', type=Path, default=ROOT / 'output/method-probes.json')
    args = parser.parse_args()
    from nyaya import Skill, TrueForge
    from nyaya.terminal import TerminalAgents
    from nyaya.codec import parse_output

    contract = {'type': 'object', 'required': ['answers', 'rationale'],
                'properties': {'answers': {'type': 'object'}, 'rationale': {'type': 'string'}},
                'additionalProperties': False}
    class Methods(TrueForge):
        def definitions(self, model):
            definitions = []
            for name in METHODS:
                text = (ROOT / 'ke' / name / 'SKILL.md').read_text().split('---', 2)[2]
                definition = TerminalAgents(model, Skill(name, text, output_contract=contract),
                                            iterations=1).definitions(model)[0]
                definition.update(role=name, name='nyaya-skill-probe-' + definition['digest'][:16])
                definitions.append(definition)
            return definitions

    args.output.parent.mkdir(parents=True, exist_ok=True)
    provider = Methods();bindings = provider.register(args.model, args.output.with_suffix('.bindings.json'))
    results = []
    for name in METHODS:
        cases = json.loads((ROOT / 'ke' / name / 'examples/probes.json').read_text())['cases']
        for case in cases:
            session = provider.session(bindings[name])['id']
            turn = provider.send(session, case['prompt'] + '\nReturn exactly a JSON object with answers and rationale.')
            deadline = time.monotonic() + 120
            while turn['state']['status'] == 'running':
                if time.monotonic() > deadline:
                    provider.cancel(session);raise TimeoutError('Probe deadline: ' + case['id'])
                time.sleep(.3);turn = provider.turn(session, turn['id'])
            if turn['state']['status'] != 'done' or turn['state'].get('required_actions'):
                raise RuntimeError('Probe did not finish: ' + str(turn['state']))
            output = parse_output(turn['state']['output']['content'])
            failures = failures_for(output.get('answers'), case['expected_answers'])
            results.append({'skill': name, 'case': case['id'], 'session': session, 'turn': turn['id'],
                            'passed': not failures, 'failures': failures, 'output': output})
            args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
            print(json.dumps({'skill': name, 'case': case['id'], 'passed': not failures}), flush=True)
    if not all(r['passed'] for r in results):raise SystemExit('Some behavior probes failed; inspect ' + str(args.output))


if __name__ == '__main__':main()
