import sys

MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

import copy
import json
import os
import re
import time
from typing import Dict, Union

import requests

PLUGIN_AUTHOR: str = "{{cookiecutter.your_name}}"

DATA_URL: str = "https://plugins.octoprint.org/plugins.json"

DATA: Dict[str, Dict[str, Union[int, str, list]]] = {}

# DATA STRUCTURE:
# {"plugin_id":
#   {
#       "total": 00,
#       "versions": {"0.1.0": 00, "0.2.0": 00}
#       "history": [
#           {"date": "2020-12-1", "total": 00, "versions": {"0.1.0": 00, "0.2.0": 00}},
#           "etc etc"
#       }
#   }
#  "etc...." for more plugins.

TODAY = time.strftime("%Y-%m-%d")

NAME_MAP: Dict[str, str] = {}
OLD_NAME_MAP: Dict[str, str] = {}
NAME_MAP_JS_PREFIX = "var names = "
RE_GITHUB = re.compile(r"(?:https?:\/\/)github.com\/(?:.*)\/(.*)")

# Read existing name map (if any)
name_file_path = os.path.abspath(os.path.join("static", "js", "name_map.js"))
if os.path.isfile(name_file_path):
    print("Reading stored name map")
    with open(name_file_path, "rt") as file:
        file.seek(len(NAME_MAP_JS_PREFIX))
        OLD_NAME_MAP = json.loads(file.read())

# Read current data (if any)
data_file_path = os.path.abspath(os.path.join("data", "stats.json"))
if os.path.isfile(data_file_path):
    print("Reading stored data")
    with open(data_file_path, "rt") as file:
        DATA = json.load(file)

# Get the data

response = requests.get(DATA_URL).json()

# iterate through, find my plugins
for plugin in response:
    if PLUGIN_AUTHOR in plugin["author"]:
        plugin_id = plugin["id"]
        print("Processing data for {}".format(plugin_id))
        # Test plugin data exists
        try:
            existing_data = DATA[plugin_id]
        except KeyError:
            # Plugin not seen before, create the dict
            DATA[plugin_id] = {"total": 0, "history": []}

        plugin_stats = copy.deepcopy(DATA[plugin_id])
        plugin_stats["total"] = plugin["stats"]["instances_month"]
        plugin_stats["title"] = plugin["title"]

        # Remove the 31st day, if relevant
        if len(plugin_stats["history"]) >= 30:
            # Check it's not been run more than once per day, latest data is not today.
            if plugin_stats["history"][29]["date"] != TODAY:
                # remove earliest data
                plugin_stats["history"].pop(0)

        if (
            not len(plugin_stats["history"])
            or plugin_stats["history"][-1]["date"] != TODAY
        ):
            # Add the latest point to the history
            plugin_stats["history"].append(
                {
                    "date": TODAY,
                    "total": plugin["stats"]["instances_month"],
                    "issues": plugin["github"]["issues"],
                }
            )

        plugin_name = plugin["title"]
        if re_match := RE_GITHUB.match(plugin["homepage"]):
            plugin_name = re_match.group(1)
        elif plugin_id in OLD_NAME_MAP:
            plugin_name = OLD_NAME_MAP[plugin_id]

        # Put the data back
        DATA[plugin_id] = plugin_stats
        NAME_MAP[plugin_id] = plugin_name

# write stats to file
with open(os.path.abspath(os.path.join("data", "stats.json")), "wt") as file:
    json.dump(DATA, file)

# write name map to file
with open(os.path.abspath(os.path.join("static", "js", "name_map.js")), "wt") as file:
    file.write(NAME_MAP_JS_PREFIX)
    json.dump(NAME_MAP, file, indent=4)

print("Done!")
