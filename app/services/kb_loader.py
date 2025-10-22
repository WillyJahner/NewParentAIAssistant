# File: kb_loader.py
# Author: William Jahner

import json
from pathlib import Path

######################################################################
# Module: load_knowledge_base
# Description: Opens a json file, converts the json data to a string,
#              and returns the string
# Input:
#   - path: The path to the json file
# Returns: The string of json data
######################################################################
def load_knowledge_base(path=Path(__file__).parent.parent.parent / "data/baby_knowledge.json") -> str:
    # Open the json file
    with open(path, "r") as f:
        data = json.load(f)
    
    # Flatten the json data into a single context string
    all_entries = []
    for category in data.values():
        for entry in category:
            all_entries.append(entry["description"])
    
    # Return the single context string
    return " ".join(all_entries)
