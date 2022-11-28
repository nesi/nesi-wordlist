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
    "possessive": False,
    "outputs": ["spellcheck", "snippet", "glossary"],
}
word_list = {}


def main():

    word_list = {}
    for yaml_list in glob.glob(YAML_FILES):
        word_list = {**read_in(yaml_list), **word_list}

    remove_if_no_long = lambda word, val: False if not val["long"] else [word, val]

    Output(
        "snippet", SNIPPET_FILE, "*[{0}]: {1[long]}\n", remove_if_no_long
    ).write_out()
    Output(
        "glossary", GLOSSARY_FILE, "### {0}:\n\t{1[long]}\n", remove_if_no_long
    ).write_out()
    Output("spellcheck", SPELLCHECK_FILE, "{0}\n").write_out()


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
        # Add plural
        if val["plural"]:
            word_list[key + "s"] = val
        # Add possessive
        if val["possessive"]:
            word_list[key + "'s"] = val
        word_list[key] = val
    return word_list


class Output:
    """
    A class used to represent an output format

    name : str
        Will be written if a word has this in its 'output'
    path : str
        Where to write this output
    pattern : str
        What to write out.
    filter : lambda
        Function to modify or skip words.

    write_out:
        write to output path
    """

    def __init__(self, name, path, pattern, *filters):
        self.name = name
        self.path = path
        self.pattern = pattern
        self.filters = filters

    def write_out(self):
        """Write output"""
        with open(self.path, "w+") as f:
            for word, val in word_list.items():
                if self.name in val["outputs"]:
                    skip = False
                    for filter in self.filters:
                        filtered = filter(word, val)
                        # If filter returned False, skip this word.
                        if filtered:
                            word, val = filtered
                        else:
                            skip = True
                    if not skip:
                        f.write(self.pattern.format(word, val))


main()
