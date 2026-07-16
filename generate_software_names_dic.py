#!/usr/bin/python3.9

import yaml
import urllib.request
import json

OUTFILE = "dic/_software_names_auto.yaml"
LISTURL = "https://raw.githubusercontent.com/nesi/modules-list/main/module-list.json"


def main():
    outdata = {}
    with urllib.request.urlopen(LISTURL) as url:
        data = json.load(url)
        for key, value in data.items():
            outdata[key] = {"long": value["description"], "possessive": True}
    with open(OUTFILE, "w", encoding="utf-8") as outfile:
        yaml.safe_dump(
            outdata,
            outfile,
            sort_keys=True,
            allow_unicode=True,
            default_flow_style=False,
        )
main()
