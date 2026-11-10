# Nyaya Skills

Reusable procedures for description, evidence-grounded inquiry and knowledge
engineering. TrueForge loads the skills; Nyaya orchestrates agents using them;
applications supply domain meaning, authorization and publication policy.

## Dialogical and knowledge-engineering skills

| Skill | Responsibility |
| --- | --- |
| `vada-samvada` | Adaptive proposer–examiner turn-taking, objections, resolution and stopping |
| `vaisheshika-description` | Entities, properties, relationships, identity and context |
| `nyaya-examination` | Evidence, inference, counterexamples and justified judgments |
| `evidence-grounding` | Claim-level source references and exact quotations |
| `draft-refinement` | Traceable revisions without concealing disagreement |
| `rdf-formalization` | Examined meaning → RDF/schema/constraints with semantic round-trip |
| `fact-extraction` | Source assertions → facts against approved vocabulary and identities |
| `query-compilation` | Natural language → grounded read-only query → explanation of actual results |

The first three distinguish the exchange protocol, the descriptive lens and the
epistemic/reasoning lens. They are computational adaptations, not historical
identity claims or a new formal logic. Description and reasoning can be combined.
Propose ↔ examine ↔ formalize is iterative; formalized is not validated or
published. The application retains those gates.

Every skill defines purpose, inputs, an adaptive question bank, a method, expected
results, mandatory acceptance gates and feedback/stopping boundaries. Weighted
quality can complement—but never replace—mandatory gates. Unknown evidence is
not a pass. Skills are reusable instructions, not permissions or proof.

`catalog.json` lists these eight skills. Each selected skill folder is
self-contained; no sibling skill is required just to load it. The original
research skill below remains a separate smoke-test pack.

## Pinned import through Nyaya

With a Nyaya checkout containing `nyaya.skillpacks`, run from that checkout:

```sh
SKILLS_REF=$(git -C ../nyaya-skills rev-parse HEAD)
.venv/bin/python -m nyaya.skillpacks build ../nyaya-skills --ref "$SKILLS_REF" --output /tmp/nyaya-thinking-skills.json
.venv/bin/python -m nyaya.skillpacks list /tmp/nyaya-thinking-skills.json
.venv/bin/python -m nyaya.skillpacks register /tmp/nyaya-thinking-skills.json
.venv/bin/python -m nyaya.skillpacks check /tmp/nyaya-thinking-skills.json
```

Build reads committed Git objects, not unreviewed working-tree edits. Registration
uses TrueForge's settings API and requires its settings/admin access. Names carry
the source commit suffix; an existing differing manifest is never overwritten.
A failed/uncertain write is not retried automatically. Registration is not evidence
of runtime skill loading.

The `list` output provides exact `registration_name` values. In Nyaya, choose a
configured sandbox environment and attach the desired registered skill names:

```sh
nyaya chat --no-tools --sandbox-environment YOUR_CONFIGURED_ENVIRONMENT --remote-skill EXACT_REGISTRATION_NAME
```

You may repeat `--remote-skill` to combine procedures. Request the exact skill
explicitly in your prompt when testing it; merely attaching it does not force its
use. Mandatory skill responsibilities also belong in the host workflow contract.
See [the synthetic Person dialogue](examples/person-dialogue.md) for prompts and
expected behavior across description, examination, formalization, facts and queries.

For manual TrueForge import, choose this repository, a skill's path from the
catalog and an exact commit ref. See below for the research smoke-test example.

## Rubric helper

```sh
python3 skills/vada-samvada/scripts/judge.py --input skills/vada-samvada/references/example-rubric.json
```

Expected: `graduate`, with weighted quality about 88.33. Changing a mandatory
assessment to fail produces `revise`, regardless of the quality score. Missing
evidence produces `clarify`; exhausting the supplied turn budget without
acceptance produces `escalate`. This helper aggregates judgments; it cannot verify
whether the supplied evidence references or assessments are actually correct.
The host must enforce real budgets, permissions and evidence checks.

## First skill: research-result-check

Summarize paired baseline/candidate measurements across seeds, check whether the
candidate improves under the declared metric direction, and produce a cautious
research result summary. The helper uses only Python's standard library.

This first skill tests instruction loading, executing a packaged helper, and
producing inspectable artifacts. It does not train models or run significance
tests. The example measurements are synthetic, not research evidence.

## Import into TrueForge

In TrueForge's GitHub skill importer, set:

| Field | Value |
| --- | --- |
| Repository | `https://github.com/dhavala-iitjmu/nyaya-skills` |
| Path | `skills/research-result-check` |
| Ref | `main` (use a commit SHA when pinning an experiment) |
| Name | `research-result-check` |

A private repository requires Git credentials configured in TrueForge. Nyaya's
GitHub login is not automatically shared with TrueForge's sandbox. Enable a
working TrueForge sandbox: repository skills are installed and executed there.
The local sandbox needs an accessible Python 3.10+ runtime; Python 3.12 is
recommended. On macOS, system Python 3.9 is too old for TrueForge's downloader.

Check that Nyaya sees the configured skill, then start a new session:

```sh
nyaya integrations
nyaya chat --no-tools --sandbox --remote-skill research-result-check
```

This leaves Nyaya's local host tools disabled; the skill uses TrueForge's sandbox.
Add `--approve-provider-tools` if you want to preauthorize provider tool approval
requests. Approval does not configure or relax the sandbox.

## Try this prompt

> Use research-result-check on these synthetic accuracy (%) measurements; higher
> is better. Seed 1: baseline 81.2, candidate 82.0. Seed 2: baseline 81.6,
> candidate 82.6. Seed 3: baseline 82.0, candidate 82.8. Save results.json,
> summary.json and report.md under output/research-result-check. Run the bundled
> helper. Explain percentage points versus relative percent improvement and
> whether these numbers establish statistical significance. Report actual
> execution results and artifact paths.

Expected observable behavior:

- The agent reads this skill and executes its bundled Python helper.
- Baseline mean is **81.6%**, candidate mean is approximately **82.4667%**.
- Mean improvement is approximately **0.8667 percentage points**, or **1.0621%**
  relative improvement. All three paired runs improve.
- The report labels the inputs synthetic and does not claim statistical significance.
- The three requested artifacts exist inside the sandbox. A prose answer alone
  is not evidence that the helper ran.

The same fixture is provided in `examples/smoke-test.json`.

## Run locally without TrueForge

From this checkout with Python 3.10+:

```sh
python3 skills/research-result-check/scripts/summarize_results.py \
  --input examples/smoke-test.json --output output/summary.json
python3 -m unittest discover -s tests -v
```

No third-party Python packages are required. Artifacts remain in `output/`, which
is ignored by Git. This verifies the helper; live TrueForge/Nyaya skill loading
is a separate check.

## Authoring more skills

Each skill belongs in `skills/<skill-name>/SKILL.md` with `name` and `description`
frontmatter. Keep its required scripts and references inside that same folder:
TrueForge may check out only the selected subdirectory. Do not make a skill rely
on this repository's root examples or another skill being present.

Add helpers when deterministic execution makes the result more reliable. Test
observable calculations and failure cases. Skills describe procedures; they do
not grant tool access or authority to publish results.

MIT licensed. See [LICENSE](LICENSE).
