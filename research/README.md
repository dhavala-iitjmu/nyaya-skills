# Research workflows (`research`)

## research-result-check

[Skill](research-result-check/SKILL.md) ·
[Synthetic measurements](research-result-check/examples/smoke-test.json) ·
[Deterministic helper](research-result-check/scripts/summarize_results.py)

This smoke-test skill summarizes paired baseline/candidate measurements across
seeds. It does not train models, establish statistical significance or turn
synthetic measurements into research evidence.

From the repository root:

```sh
python3 research/research-result-check/scripts/summarize_results.py --input research/research-result-check/examples/smoke-test.json --output output/summary.json
```

Expected: baseline mean 81.6%, candidate mean about 82.4667%, improvement about
0.8667 percentage points or 1.0621% relative. All three synthetic pairs improve.

For TrueForge, import `research/research-result-check` at an exact source commit.
Or build a Nyaya bundle with `--category research`. Native loading needs an
existing sandbox; attach the exact registered name to the agent.

Suggested prompt:

> Use the attached research-result-check skill on its bundled synthetic example.
> Run the helper, save an auditable summary and explain percentage points versus
> relative improvement. Do not claim statistical significance. Report actual
> artifact paths and execution results.

See [repository setup and registration](../README.md). The skill directory is
self-contained, including its example data and helper.
