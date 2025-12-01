# File: list_service.py
# Author: William Jahner

import re
from collections import defaultdict

######################################################################
# Module: get_milestone_list
# Description: Extracts and returns a list of developmental milestones
#              for a specified age from the knowledge base.
# Input:
#   - knowledge_base: The flattened knowledge base as a list of
#                     labeled text entries.
#   - question: The user's question containing the age.
# Returns:
#   - A list of developmental milestones for the specified age,
#     formatted as a string. If the age is not found or invalid,
#     it returns an appropriate error message.
######################################################################
def get_milestone_list(knowledge_base, question):
    # Extract age from question ("6 months", "4 month old", etc.)
    match = re.search(r"\b(\d{1,2})\s*month", question.lower())
    if not match:
        error_return = "Sorry, I couldn't determine an age from your question. " + \
                       "Note that the age should be specified in months."
        return error_return

    age = f"{match.group(1)} months"

    # Prepare storage for categories and milestone items
    categories = defaultdict(list)

    # Look through the flattened knowledge base
    for label, text in knowledge_base:
        parts = label.split(" - ")

        if len(parts) != 3:
            continue  # skip entry if it does not match the expected format

        main_category, entry_age, sub_category = parts

        if main_category != "milestones":
            continue

        if entry_age == age:
            categories[sub_category].append(text)

    # Handle case where age is valid but no milestones are found
    if not categories:
        error_return = f"No milestone data found for {age}. " + \
                        "Note that the milestone data is from the American Academy of Pediatrics (AAP), " + \
                        "which specifies milestones at 2, 4, 6, 9, and 12 months."
        return error_return

    # Format output nicely
    output = [f"Developmental milestones for {age}:\n"]
    for category, items in categories.items():
        readable_category = category.replace("_", "/").title()
        output.append(f"{readable_category}:")
        for item in items:
            output.append(f"- {item}")
        output.append("")  # blank line between categories

    final_list = "\n".join(output)
    return final_list
