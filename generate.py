#!/usr/bin/python3.9

import yaml
import glob

YAML_FILES = "dic/*.y*ml"
SPELLCHECK_FILE = "outputs/dictionary.txt"
SNIPPET_FILE = "outputs/snippets.md"
GLOSSARY_FILE = "outputs/Glossary.md"

default_values = {
    "long": "",
    "checkcase": True,
    "plural": False,
    "spellcheck": True,
    "snippet": True,
    "glossary": True,
}
word_list = {}


def main():

    word_list = {}
    for yaml_list in glob.glob(YAML_FILES):
        word_list = {**read_in(yaml_list), **word_list}

    write_out(SNIPPET_FILE, "snippet", "*[{0}]: {1[long]}\n")
    write_out(GLOSSARY_FILE, "glossary", "### {0}:\n\t{1[long]}\n")
    write_out(SPELLCHECK_FILE, "spellcheck", "{0}\n")


def read_in(yaml_file):
    """parse yaml file with defaults"""
    with open(yaml_file, "r") as f:
        yaml_list = yaml.load(f, Loader=yaml.FullLoader)

    for key, val in yaml_list.items():
        # Coalese null
        val = val or {}
        # fill in defaults.
        for k, v in default_values.items():
            if k not in val:
                val[k] = v
        # Disable glos and snip if no long value.
        if not val["long"]:
            val["glossary"] = False
            val["snippet"] = False
        # Add plural
        if val["plural"]:
            word_list[key + "s"] = val
        word_list[key] = val
    return word_list


def write_out(output, key, pattern):
    """Write output"""
    with open(output, "w+") as f:
        for word, val in word_list.items():
            if val[key]:
                f.write(pattern.format(word, val))


main()
