A wordlist for use across various projects.

## How to use.

The yaml files in `dic/` inform several different things (at present). Editing any of these files should trigger regeneration of the outputs.

### Parameters

| Key      | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| `long` | string | Long description, multiple sentance, markdown? suitable for a glossary entry or similar. | `""` |
| `short` | string | Short description, expanded acronym, one sentance summary. | `""` |
| `checkcase` | bool | [NOT IMPLIMENTED] Whether a difference in capitalisation should be considered a typo. | `True` |
| `plural` | bool | Whether the plural of this word is considered valid | False |
| `possessive` | bool | Whether the plural of this word is considered valid | False |
| `outputs` | list string | Which output patterns this word should be included in | `["spellcheck", "snippet", "glossary"]` |

Defaults currently hardcoded in [`generate.py`](./generate.py)

### Aliases

Word aliases can be created with standard YAML syntax.

* The referenced word must include a tag,`&value`.
* The alias word must equal the tag `*value`.

### Example
Example entry and alias.
```
- HPC: &hpc
   short: High Performance Computing/Computer
   long: Like a regular computer, but larger. Primarily used for heating data centers.
   checkcase: false 
   outputs: ["glossary, "spellcheck"] 
- supercomputer: *hpc #This is an alias of HPC.
```

## Implimentation

Running `./generate.py` should create several outputs based on defined patterns. 

Currently these are the outputs;

### `snippets.md` 
`"snippet"`

Used for the generation of snippets (for use with mkdocs-material tooltips and glossary ). 

A word will not be included in snippets if `snippets: false` or `long:` is empty.

For a page to impliment snippets it must include 
```
--8<-- "includes/glossary/.dictionary.md"
```
at the page footer. (consider adding to page material).


#### Output Format:

```
*[tfe]: The Full Explanation 
*[smth-e]: Something Else
*[smthe]: Something Else
```

#### Currently used in
* [mkdocs](https://git.hpcf.nesi.org.nz/nesi-apps/mkdocs)

### `dictionary.txt` 
`"spellcheck"`

[NOT IMPLIMENTED] Will be case sensitive unless `checkcase: false` 

#### Output Format:
```
tfe
smth-e
smthe
```
#### Currently used in
* [zendesk-macros](https://git.hpcf.nesi.org.nz/nesi-apps/zendesk-macros)
* [mkdocs](https://git.hpcf.nesi.org.nz/nesi-apps/mkdocs)
* [migratedocs](https://git.hpcf.nesi.org.nz/cwal219/migratedocs)

### `Glossary.md`
`"glossary"`

Nicely formatted markdown page for human reading.

All words will be included along with any aliases unless `long:` is empty.

#### Output Format:

```
#### - tfe : 
The Full Explanation.
#### - smth-e, smthe : 
Something Else
```
#### Currently used in
* This repo I guess?

#### Could be used in software carpentrty lessons
