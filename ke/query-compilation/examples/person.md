# Query: synthetic Person example

## Input

> Accepted snapshot: ex:Person, ex:name, ex:Alice1 a ex:Person, ex:Alice1 ex:name "Alice". Compile "Is Alice1 a Person?" to read-only SPARQL ASK.

## Expected behavior

Ground Alice1 and Person in the supplied namespace/snapshot. Do not substitute Alice or Alice2. Do not invent an answer before actual query results are supplied.

The host supplies exact scope, namespace bindings, output contract and authorized tools. This example grants no writes or publication authority.
