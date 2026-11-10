# Person: propose, examine, formalize

This is a synthetic skill evaluation case, not a preloaded ontology or application database.

## Propose

> Describe Person as a class. A person may have a textual name. Names are not unique identifiers and a name is optional. Do not add Alice as a fact yet. Use vaisheshika-description and vada-samvada. Return a minimal draft, positive/negative examples and consequential questions only.

Expected: a natural-language draft distinguishing Person, a name property and individual identity. It must not infer a required or unique name, invent biographical facts, or treat an unspecified name as a contradiction.

## Examine

> Use nyaya-examination to review the draft. Two people can both be named Alice. Can the description represent them without merging their identity? A missing name is not evidence that someone is not a person. Ask only questions that could change the meaning. Refine the draft if needed, recording the objection and resolution.

Expected: identity remains separate from label. Optionality and unknowns survive. No manufactured disagreement is required when the original draft already handles these cases.

## Formalize

> Use rdf-formalization. Encode the examined schema as Turtle in namespace https://example.org/people/. Use RDFS only. Include Person and an optional textual name property; do not assert example people. Explain the Turtle back in natural language. Do not claim validation or publication.

Expected: a Person class and a name property with appropriate intended meaning. No invented cardinality, mandatory name, unique-name constraint, Alice instance, database write or validation claim. RDFS domain/range entailments must not be described as SHACL constraints.

## Populate and query

> Use fact-extraction against that schema. Source S1 says exactly "Alice1 is a person named Alice." Propose a distinct Alice1 individual with that evidence. Do not equate it with any person named Alice.

> Use query-compilation: is Alice1 a Person? Ground every term in the supplied schema and accepted identity snapshot. Return a read-only SPARQL ASK query. Explain a result only after the host supplies the actual result.

These exercises require the application to provide accepted vocabulary, identity bindings, output contracts and authorized tools. The skills do not create a ledger or authorize publication.
