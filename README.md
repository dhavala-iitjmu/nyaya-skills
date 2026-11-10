# Nyaya Skills

The companion skill library for [Nyaya](https://github.com/dhavala-iitjmu/nyaya),
a standalone agentic harness and reasoning framework built on TrueForge. Nyaya
coordinates agents, tools, review and bounded workflows; this library supplies
reusable, versioned procedures, examples and supporting scripts for those agents.

The skills cover knowledge engineering and research workflows. TrueForge loads
selected `SKILL.md` packs; Nyaya composes their methods into agents and workflows.
Applications supply domain meaning, authorized tools and publication policy.

## Categories

| Category | Contents |
| --- | --- |
| [ke — Knowledge engineering](ke/README.md) | Dialogue, description, examination, grounding, refinement, RDF formalization, fact extraction and query compilation |
| [research — Research workflows](research/README.md) | Paired experimental-result checking smoke test |

Each skill lives at `<category>/<skill-name>/SKILL.md`. Examples, scripts and
references belong inside that skill's directory so importing a single folder
remains self-contained. Each category has its own README and examples index.
There are no uncategorized root-level skills or examples.

`catalog.json` lists every skill with `category`, `family`, repository-relative
path and description. Skill identifiers are stable; paths are category-qualified.

## Import a category through Nyaya

Run from your Nyaya checkout:

```sh
SKILLS_REF=$(git -C ../nyaya-skills rev-parse HEAD)
.venv/bin/python -m nyaya.skillpacks build ../nyaya-skills --ref "$SKILLS_REF" --category ke --output /tmp/nyaya-ke.json
.venv/bin/python -m nyaya.skillpacks list /tmp/nyaya-ke.json
.venv/bin/python -m nyaya.skillpacks register /tmp/nyaya-ke.json
.venv/bin/python -m nyaya.skillpacks check /tmp/nyaya-ke.json
```

Omit `--category` to include all categories. Commit refs are immutable; registration
names include the commit suffix and differing existing manifests are never
overwritten. `TRUEFORGE_BASE_URL` and optional `TRUEFORGE_TOKEN` configure server
access. Registration requires settings/admin access; native Git skill loading
requires a configured TrueForge sandbox. Registration alone is not proof of use.

For manual import, use this repository, an exact commit and the path from the
catalog, for example `ke/vaisheshika-description`. Attach the resulting exact
registry name to an agent. Existing registrations pinned to older commits remain
reproducible; new category paths require new pinned registrations.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
python3 ke/vada-samvada/scripts/judge.py --input ke/vada-samvada/examples/rubric.json
python3 research/research-result-check/scripts/summarize_results.py --input research/research-result-check/examples/smoke-test.json --output output/summary.json
```

The helpers use only Python's standard library. They evaluate supplied inputs,
not the factual truth of evidence or live model quality. Live TrueForge loading
and agent behavior remain separate acceptance checks.

MIT licensed. See [LICENSE](LICENSE).
