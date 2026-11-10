# Nyaya Skills

Reusable skills for AI research scientists, imported into TrueForge and used
through Nyaya. Start with a small, verifiable research workflow before expanding
into experiment design, reproducibility checks and research reporting.

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
