#!/usr/bin/env python3

import sys

import yaml


class NullSafeDumper(yaml.SafeDumper):
    pass


def represent_none(dumper, _value):
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


NullSafeDumper.add_representer(type(None), represent_none)


def main(path):
    with open(path, encoding="utf-8") as infile:
        data = yaml.safe_load(infile) or {}
    with open(path, "w", encoding="utf-8") as outfile:
        yaml.dump(
            data,
            outfile,
            Dumper=NullSafeDumper,
            sort_keys=True,
            allow_unicode=True,
            default_flow_style=False,
        )


if __name__ == "__main__":
    main(sys.argv[1])