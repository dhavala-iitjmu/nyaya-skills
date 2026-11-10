# Knowledge engineering (`ke`)

These skills support **propose ↔ examine ↔ formalize**, with evidence and revision
throughout. Vaisheshika-inspired description supplies a descriptive lens;
Nyaya-inspired examination supplies an epistemic/reasoning lens; vāda–saṃvāda
organizes the exchange. Applications and domain experts supply actual content.
These are computational adaptations, not historical equivalence or a new logic.

| Skill | Family | Examples |
| --- | --- | --- |
| [vada-samvada](vada-samvada/SKILL.md) | dialogue | [Person example](vada-samvada/examples/person-dialogue.md) |
| [vaisheshika-description](vaisheshika-description/SKILL.md) | description | [Person example](vaisheshika-description/examples/person.md) |
| [nyaya-examination](nyaya-examination/SKILL.md) | reasoning | [Person example](nyaya-examination/examples/person.md) |
| [evidence-grounding](evidence-grounding/SKILL.md) | reasoning | [Person example](evidence-grounding/examples/person.md) |
| [draft-refinement](draft-refinement/SKILL.md) | description | [Person example](draft-refinement/examples/person.md) |
| [rdf-formalization](rdf-formalization/SKILL.md) | formalization | [Person example](rdf-formalization/examples/person.md) |
| [fact-extraction](fact-extraction/SKILL.md) | population | [Person example](fact-extraction/examples/person.md) |
| [query-compilation](query-compilation/SKILL.md) | query | [Person example](query-compilation/examples/person.md) |

The [dialogue example](vada-samvada/examples/person-dialogue.md) connects multiple
skills; each other skill has its own focused input and expected outcome. The
[rubric fixture](vada-samvada/examples/rubric.json) exercises mandatory gates and
weighted quality using the dialogue skill's [helper](vada-samvada/scripts/judge.py).

## Contracts and boundaries

Each skill defines purpose, inputs, adaptive questions, method, expected outputs,
acceptance gates and stopping conditions. Unknown evidence does not pass; quality
cannot offset a mandatory failure. Formalized is not validated or published.
Output schemas, tool permissions, budgets and publication remain host contracts.

## Use this category

From a Nyaya checkout, use `python -m nyaya.skillpacks build ../nyaya-skills
--ref COMMIT_SHA --category ke --output /tmp/nyaya-ke.json`, then register/check
that bundle. See the [repository import directions](../README.md). Native CLI
use is `nyaya chat --no-tools --sandbox --remote-skill EXACT_REGISTRATION_NAME`.
Repeat `--remote-skill` to compose methods, and request them explicitly when
checking progressive loading.

For TrueForge's manual importer, choose the exact `ke/<skill-name>` directory,
not the category root. Every selected folder includes its own examples and any
required helper; no root-level example or sibling skill is needed to load it.
