---
name: skypilot
description: Submit and inspect experiments on explicitly selected SkyPilot compute using Bash, synchronize code and data, collect artifacts, and manage the requested cluster lifecycle. Use for SkyPilot-backed CPU or GPU jobs on Kubernetes, Slurm, or supported clouds.
---

# SkyPilot compute

Use the existing `sky` CLI through an authorized Bash tool. This skill is
operating knowledge, not an execution provider or a permission grant. No MCP
service beyond Nyaya's existing tool bridge or second agent harness is required.

## Establish the target

Check `sky --version`, `sky api info`, and the relevant command's `--help`.
Use the user's selected infrastructure and credentials. For a laptop test,
`sky local up --name NAME --num-nodes 1 --no-gpus` creates local Kubernetes;
check its context with `kubectl config get-contexts` and
`sky check kubernetes`. Pin tasks to `k8s/CONTEXT`, including subsequent launches.
If a local prerequisite fails, report it; do not fall back to a paid cloud.

An existing endpoint may already be selected. Do not log into a different API
server, change shared credentials, install software, or tear down resources
unless that setup or lifecycle action is within the user's request.

## Submit, observe, collect

1. Write a task YAML with explicit resources, code `workdir`, setup and run
   commands. Match CLI syntax to the installed version. Sync only the experiment
   source and required small inputs; exclude virtual environments, credentials,
   framework state and previous output directories.
2. For interactive experiments use `sky launch -c NAME task.yaml -y -d`, then
   `sky exec NAME task.yaml -d` for another job on that cluster. For unattended
   production work, consider `sky jobs launch`; consult its installed help for
   lifecycle and recovery behavior. Scope resources and concurrency to the task.
3. Record the actual cluster, infrastructure context, job/request identifiers,
   code revision, input version and artifact locations. A submitted request is
   not a completed experiment. Poll with bounded, non-following status/log
   commands rather than holding a Bash tool open for an entire training run.
   Detached `-d` skips job-log following but may still wait for provisioning.
   When the CLI supports `--async`, use it to submit a long provisioning request
   and inspect its actual request ID with `sky api status` before inspecting jobs.
4. Inspect `sky queue NAME`, `sky logs NAME JOB_ID --status`, and
   `sky logs NAME JOB_ID --no-follow` as supported. Record failed jobs as failures.
   After a timeout or uncertain submission, inspect existing jobs before
   resubmitting: submission can have succeeded even when the caller timed out.
5. Collect actual outputs separately from logs. For a development cluster,
   SkyPilot configures SSH access; `rsync`/`scp` can retrieve paths from the remote
   workdir. Verify metrics, checksums and expected files independently. Large
   artifacts can remain in persistent storage with references returned locally.

## Data and lifetime

`workdir` stages code and local files for a job; it is not a general bidirectional
dataset sync. Repeated `sky exec` workdir syncs can overwrite remote changes.
Use input versions and separate output paths. Data in the same development pod
can survive successive jobs but is not guaranteed to survive cluster teardown.

For larger workloads, use supported bucket mounts/copies or persistent volumes
near compute. Pin datasets, validate transferred bytes, and keep inputs read-only
where practical. Object-store mounts differ from POSIX filesystems; choose local
scratch or an appropriate filesystem for rename/append/random-write workloads.
Do not assume an arbitrary S3-compatible endpoint has native SkyPilot support.

Respect requested retention: leave a testing cluster available when requested,
or tear down only the exact resources created for the task. `sky down NAME`
removes a SkyPilot workload; `sky local down` removes the local Kubernetes
cluster. Check installed help for selecting a named local cluster. Never use a
wildcard cleanup against unrelated clusters or volumes.

## Local smoke test

Use [the tiny experiment](examples/experiment.py) with a CSV containing `x,y`
columns. It fits a line on the first 24 rows and compares held-out MAE with a
training-mean baseline. Run `python3 experiment.py --input data.csv --output output`,
then `python3 experiment.py --verify output` in a second job. Retrieve `output/`
and verify it locally. Completion establishes code execution, staging, artifact
integrity and same-cluster reuse, not GPU support or real scientific progress.

## Sources and relationship to upstream

This concise Nyaya skill is independently authored, using SkyPilot's public
interfaces; it is not a vendored copy of its broader official skill.
Upstream reference reviewed at commit `54c2f00c2f579b80475505398462598c11746d5b`:
[official skill](https://github.com/skypilot-org/skypilot/blob/54c2f00c2f579b80475505398462598c11746d5b/agent/skills/skypilot/SKILL.md).
For advanced operations use [SkyPilot documentation](https://docs.skypilot.ai/en/latest/),
especially [local Kubernetes](https://docs.skypilot.ai/en/latest/reference/kubernetes/kubernetes-deployment.html)
and [storage](https://docs.skypilot.ai/en/latest/reference/storage.html).
