# File: kb_loader.py
# Author: William Jahner

import json
from pathlib import Path

######################################################################
# Module: load_knowledge_base
# Description: Loads a hierarchical baby knowledge base JSON file and
#              flattens it into a list of labeled text entries for use
#              in AI retrieval or embedding.
# Input:
#   - path: The path to the JSON file.
# Returns:
#   - A list of tuples [(label, text), ...]
######################################################################
def load_knowledge_base(path=Path(__file__).parent.parent.parent / "data/baby_knowledge.json"):
    with open(path, "r") as f:
        data = json.load(f)

    knowledge_entries = []

    # Loop through top-level categories (e.g., "milestones", "feeding", etc.)
    for main_category, category_data in data.items():
        # Example: category_data = { "3 months": {...}, "6 months": {...}, etc. }
        for subkey, subdata in category_data.items():
            # If the subdata is nested by subcategories (like milestone types)
            if isinstance(subdata, dict):
                for subcat, entries in subdata.items():
                    # Add each entry with a descriptive label
                    for e in entries:
                        label = f"{main_category} - {subkey} - {subcat}"
                        knowledge_entries.append((label, e))
            # Otherwise, it’s a simple list
            elif isinstance(subdata, list):
                for e in subdata:
                    label = f"{main_category} - {subkey}"
                    knowledge_entries.append((label, e))

    return knowledge_entries
