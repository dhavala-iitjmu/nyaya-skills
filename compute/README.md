# Compute (`compute`)

| Skill | Purpose | Example |
| --- | --- | --- |
| [skypilot](skypilot/SKILL.md) | Operate selected SkyPilot infrastructure through an authorized Bash tool | [Tiny CPU experiment and artifact verifier](skypilot/examples/experiment.py) |

Import `compute/skypilot` through TrueForge at an exact source commit, or compose
its instructions into a Nyaya local JSON skill. Native TrueForge skill helpers
run in its sandbox; the local JSON Skill + Bash path uses the host's SkyPilot
installation and credentials. A skill does not install compute tooling or grant
execution permissions.

The local PoC uses a single CPU-only Kubernetes node created by `sky local up`.
It establishes code/data staging, real job execution, result retrieval and reuse
of outputs in a second job on the same cluster. It does not test cloud GPUs,
large-data performance or persistent-volume recovery after cluster deletion.

See [Nyaya's local SkyPilot tutorial](https://github.com/dhavala-iitjmu/nyaya/blob/main/docs/skypilot-local.md)
for setup, invocation and observed validation results.
