# NeSI Wordlist

A wordlist for use across various projects.

The yaml files in `dic/` inform several different things (at present). 
Editing any of these files should trigger regeneration of the outputs.

## Adding Words

Choose a category file from `dic/` (or add a new one if required).
The yaml files are dictionaries, where the key is the word in question, and the parameters are as below.

### Parameters

| Key          | Type   | Description                                                                              | Default                                 |
| ------------ | ------ | ---------------------------------------------------------------------------------------- | --------------------------------------- |
| `long`       | string | Long description, multiple sentance, markdown? suitable for a glossary entry or similar. | `""`                                    |
| `short`      | string | Short description, expanded acronym, one sentance summary.                               | `""`                                    |
| `checkcase`  | bool   | [NOT IMPLIMENTED] Whether a difference in capitalisation should be considered a typo.    | `True`                                  |
| `plural`     | bool   | Whether the plural of this word is considered valid.                                     | `False`                                 |
| `possessive` | bool   | Whether the possessive of this word is considered valid.                                 | `False`                                 |
| `outputs`    | list   | Output patterns to use.                                                                  | `["spellcheck", "snippet", "glossary"]` |

Defaults currently hardcoded in [`generate.py`](./generate.py)

### Automatically Generated inputs

`software_names.yaml` is generated by running `generate_software_names_dic.py`

### Aliases

Word aliases can be created with standard YAML syntax.

* The referenced word must include a tag,`&value`.
* The alias word must equal the tag `*value`.

### Example

Example entry and alias.

```yaml
- HPC: &hpc
   short: High Performance Computing/Computer
   long: Like a regular computer, but larger. Primarily used for heating data centers.
   checkcase: false 
   plural: true 
   outputs: ["glossary, "spellcheck"] 
- supercomputer: *hpc #This is an alias of HPC.
```

### Dictionaries

| Name                        | Usage                                                     | Example                           |
| --------------------------- | --------------------------------------------------------- | --------------------------------- |
| `_software_names_auto.yaml` | Automatically generated from module list.                 | DON'T MANUALLY EDIT               |
| `acronyms.yaml`             | You know what an                                          |                                   |
| `commands.yaml`             | Command line commands.                                    | `mv`, `scp` etc                   |
| `inexplicably-absent.yaml`  | Words that aren't in aspell but really should be.         |                                   |
| `jargon.yaml`               | Technical Jargon                                          | `Hyperthreading`, `Supercomputer` |
| `misc.yaml`                 |                                                           |                                   |
| `proper_names.yaml`         | Companies, people, etc                                    | `ZenDesk`, `Google`               |
| `software_names.yaml`       | Software not in our module list.                          |                                   |
| `te_reo.yaml`               | Many spellcheckers don't support multiple core languages. | `mihi`                            |

## Implimentation

Running `./generate.py` should create several outputs based on defined patterns.

Currently these are the outputs;

### `snippets.md`

`"snippet"`

Used for the generation of snippets (for use with mkdocs-material tooltips and glossary ).

A word will not be included in snippets if `snippets: false` or `long:` is empty.

For a page to impliment snippets it must include

```md
--8<-- "includes/glossary/.dictionary.md"
```

at the page footer. (consider adding to page material).

#### Output Format

```md
*[tfe]: The Full Explanation 
*[smth-e]: Something Else
*[smthe]: Something Else
```

#### Currently used in

* [mkdocs](https://git.hpcf.nesi.org.nz/nesi-apps/mkdocs)

### `dictionary.txt`

`"spellcheck"`

[NOT IMPLIMENTED] Will be case sensitive unless `checkcase: false`

#### Dictionary Output Format

```md
tfe
smth-e
smthe
```

#### Dictionary currently used in

* [zendesk-macros](https://git.hpcf.nesi.org.nz/nesi-apps/zendesk-macros)
* [mkdocs](https://git.hpcf.nesi.org.nz/nesi-apps/mkdocs)
* [support docs](https://github.com/nesi/support-docs-concept)
* [migratedocs](https://git.hpcf.nesi.org.nz/cwal219/migratedocs)

### `Glossary.md`

`"glossary"`

Nicely formatted markdown page for human reading.

All words will be included along with any aliases unless `long:` is empty.

#### Glossary Output Format

```md
#### - tfe : 
The Full Explanation.
#### - smth-e, smthe : 
Something Else
```

#### glossary currently used in

* [support docs](https://github.com/nesi/support-docs-concept)
* This repo I guess?

#### Could be used in software carpentrty lessons
