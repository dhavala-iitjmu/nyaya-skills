---
name: research-result-check
description: Check paired baseline and candidate measurements from an AI experiment, compute descriptive improvements across seeds, and draft a cautious result summary. Use for a quick sanity check of supplied results, not for running training or claiming statistical significance.
---

# Research result check

Turn a small set of paired experimental measurements into an auditable summary.
Use Python 3.10+; the helper needs only the standard library.

## Inputs and scope

Obtain the metric name, whether higher or lower is better, and baseline/candidate
measurements paired by seed. Do not guess direction or pairing. If the user has
not supplied measurements, ask for them; use synthetic values only when the user
requests a demonstration and label them synthetic.

Use this JSON shape, preserving the supplied values and metric units:

```json
{
  "metric": "accuracy (%)",
  "direction": "higher",
  "runs": [
    {"seed": 1, "baseline": 81.2, "candidate": 82.0},
    {"seed": 2, "baseline": 81.6, "candidate": 82.6},
    {"seed": 3, "baseline": 82.0, "candidate": 82.8}
  ]
}
```

If runs are unpaired or the experiment conditions differ, explain the limitation
instead of forcing them into this paired calculation. Metric values alone do
not establish equal datasets, compute budgets, tuning effort or evaluation code.

## Calculate and report

1. Save the supplied input as `results.json` in the requested output directory.
2. Locate this skill's `scripts/summarize_results.py` relative to this `SKILL.md`.
   Execute it rather than estimating numbers in prose:

   ```sh
   python3 /path/to/research-result-check/scripts/summarize_results.py \
     --input results.json --output summary.json
   ```

   Replace the example path with the actual mounted skill path. On invalid input,
   report the validation error and request corrected measurements. Do not silently
   drop a run or substitute a measurement.
3. Write a short `report.md` in the same output directory. Include:
   - Metric, direction, number of paired runs, and whether values are synthetic.
   - Baseline and candidate means, sample standard deviations, mean signed
     improvement, and improved/tied/worse run counts.
   - Distinguish a percentage-point difference from relative percent improvement
     for percentage-valued metrics. Positive signed improvement always means
     better performance under the declared direction.
   - Limitations and the next useful check, such as more independent seeds or
     verifying that evaluations used the same data and compute budget.

A single pair has no estimable sample standard deviation; report it as unavailable.
The helper computes descriptive statistics only. Neither consistent improvements
nor a positive mean difference establishes statistical significance, causality,
generalization or a publishable claim. Do not invent a p-value or confidence
interval. Do not call a standard deviation a standard error or confidence interval.

Return the actual artifact paths and execution status. Keep any supplied data
and generated files in the authorized output location; this skill does not
require downloads, training, external services or extra packages.
