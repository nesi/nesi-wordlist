#!/usr/bin/python3.9

import yaml
import glob
import re

YAML_FILES = "dic/*.y*ml"
SPELLCHECK_FILE = "outputs/dictionary.txt"
SNIPPET_FILE = "outputs/snippets.md"
GLOSSARY_FILE = "outputs/glossary.md"

default_values = {
    "long": "",
    "short": "",
    "checkcase": True,
    "plural": False,
    "possessive": False,
    "outputs": ["spellcheck", "snippet", "glossary"],
}


def main():
    word_list = read_in(YAML_FILES)
    Output(
        "snippet",
        SNIPPET_FILE,
        "*[{0}]: {1[long]}\n",
        remove_if_no_long,
        pluralise,
        possessivise,
    ).write_out(word_list)
    Output(
        "glossary", GLOSSARY_FILE, "## {0}:\n\n{1[long]}\n\n", remove_if_no_long
    ).write_out(word_list)
    Output("spellcheck", SPELLCHECK_FILE, "{0}\n", pluralise, possessivise).write_out(word_list)


def read_in(yaml_files):
    """parse yaml file with defaults"""
    word_list = {}
    for yaml_file in glob.glob(yaml_files):

        with open(yaml_file, "r") as f:
            yaml_list = yaml.load(f, Loader=yaml.FullLoader)

        for key, val in yaml_list.items():
            # Coalese null
            val = val or {}

            if type(val) is str:
                val = {"short": val}

            # fill in defaults.
            for k, v in default_values.items():
                if k not in val:
                    val[k] = v
            if key in word_list.keys():
                for k, v in val.items():
                    if type(v) is bool:
                        word_list[key][k] = any([word_list[key][k], v])
                    elif type(v) is list:
                        word_list[key][k] = word_list[key][k] + v
                    else:
                        word_list[key][k] = max([word_list[key][k], v], key=len)
                print(f"warning: Duplicate dictionary entry '{key}', in {yaml_file} and 1 other.")
                print(f"Merged into: {word_list[key]}")

            else:
                word_list[key] = val

    word_list = dict(sorted(word_list.items()))
    return word_list

# Filters


def remove_if_no_long(k, v):
    if v["long"]:
        yield k, v


def pluralise(k, v):
    # Add plural
    if v["plural"]:
        # Make it plural by adding es in end
        if re.search('[sxz]$', k) or re.search('[^aeioudgkprt]h$', k):
            yield re.sub('$', 'es', k), v
        # Make it plural by removing y from end adding ies to end
        elif re.search('[aeiou]y$', k):
            yield re.sub('y$', 'ies', k)
        # Make the plural of word by adding s in end
        else:
            yield k + "s", v
    yield k, v


def possessivise(k, v):
    # Add possessive
    if v["possessive"]:
        yield k + "'s", v
    yield k, v


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

    def apply_filter(self, filter, word_list):
        for word, val in word_list.items():
            if self.name in val["outputs"]:
                for kp in filter(word, val):
                    if kp:
                        yield kp

    def write_out(self, word_list):
        """Write output"""
        with open(self.path, "w+") as f:
            for filter in self.filters:
                word_list = {k: v for k, v in self.apply_filter(filter, word_list)}
            for word, val in word_list.items():
                f.write(self.pattern.format(word, val))


main()
