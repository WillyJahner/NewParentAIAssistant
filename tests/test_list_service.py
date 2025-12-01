# File: test_list_service.py
# Author: William Jahner

import unittest
from app.services.list_service import get_milestone_list

######################################################################
# Class: TestGetMilestoneList
# Description: This class is for testing list_service.py functionalities.
######################################################################
class TestGetMilestoneList(unittest.TestCase):

    ######################################################################
    # Module: test_age_not_found
    # Description: Tests that the correct error message is returned when
    #              no age is found in the question.
    ######################################################################
    def test_age_not_found(self):
        # Set up an empty knowledge base and a question without age
        kb = []
        question = "What milestones should my baby reach?"

        # Call get_milestone_list
        result = get_milestone_list(kb, question)

        # Verify the error message
        self.assertIn("Sorry, I couldn't determine an age from your question", result)
        self.assertIn("Note that the age should be specified in months", result)

    ######################################################################
    # Module: test_no_milestones_for_valid_age
    # Description: Tests that the correct error message is returned when
    #              an age is found but there are no matching entries for
    #              that age in the knowledge base.
    ######################################################################
    def test_no_milestones_for_valid_age(self):
        # Set up a knowledge base without entries for 5 months
        kb = [
            ("milestones - 4 months - social_emotional", "Smiles on his own to get your attention"),
            ("milestones - 6 months - movement_physical", "Rolls from tummy to back"),
        ]
        question = "What are milestones for a 5 month old?"

        # Call get_milestone_list
        result = get_milestone_list(kb, question)

        # Verify the error message
        self.assertIn("No milestone data found for 5 months", result)
        self.assertIn("Note that the milestone data is from the American Academy of Pediatrics (AAP),", result)
        self.assertIn("which specifies milestones at 2, 4, 6, 9, and 12 months", result)

    ######################################################################
    # Module: test_milestone_extraction_success
    # Description: Tests that the milestone is correctly retrieved for the
    #              matching age.
    ######################################################################
    def test_milestone_extraction_success(self):
        # Set up a knowledge base with multiple entries
        kb = [
            ("milestones - 6 months - social_emotional", "Smiles at people"),
            ("milestones - 6 months - movement_physical", "Sits without support"),
            ("milestones - 4 months - movement_physical", "Holds head steady"),
            ("feeding - 6 months - solids", "Introduce purees"),
        ]

        # Ask a question for 6 month milestones
        question = "What are the milestones for a 6 month old?"

        # Call get_milestone_list
        result = get_milestone_list(kb, question)

        # Verify the output contains the correct header
        self.assertIn("Developmental milestones for 6 months", result)

        # Verify that the output contains the correct categories (formatted)
        self.assertIn("Social/Emotional:", result)
        self.assertIn("Movement/Physical:", result)

        # Verify that the output contains the correct milestone items
        self.assertIn("- Smiles at people", result)
        self.assertIn("- Sits without support", result)

        # Verify that the output does NOT include unrelated categories like feeding
        self.assertNotIn("Introduce purees", result)

        # Verify that the output does NOT include other ages
        self.assertNotIn("Holds head steady", result)

    ######################################################################
    # Module: test_handles_underscore_category_names
    # Description: Tests that the underscore category names are converted
    #              to readable text.
    ######################################################################
    def test_handles_underscore_category_names(self):
        # Set up a knowledge base with underscore in category names
        kb = [
            ("milestones - 6 months - movement_physical", "Rolls from tummy to back")
        ]

        # Call get_milestone_list
        result = get_milestone_list(kb, "What are the milestones for a 6 month old?")

        # Verify that "movement_physical" is converted to "Movement/Physical"
        self.assertIn("Movement/Physical:", result)

    ######################################################################
    # Module: test_skips_malformed_labels
    # Description: Tests that the labels that do not follow the expected
    #              3-part format are skipped.
    ######################################################################
    def test_skips_malformed_labels(self):
        # Set up a knowledge base with 1 valid and 1 invalid label
        kb = [
            ("milestones - 6 months", "Invalid label format"),
            ("milestones - 6 months - movement_physical", "Rolls from tummy to back")
        ]

        # Call get_milestone_list
        result = get_milestone_list(kb, "What are the milestones for a 6 month old?")

        # Verify that the output contains the valid item
        self.assertIn("Rolls from tummy to back", result)

        # Verify that the output does NOT contain the invalid item
        self.assertNotIn("Invalid label format", result)

    ######################################################################
    # Module: test_multiple_items_grouped_under_same_category
    # Description: Tests that multiple items under the same category are
    #              grouped together.
    ######################################################################
    def test_multiple_items_grouped_under_same_category(self):
        # Set up a knowledge base with multiple items under the same category
        kb = [
            ("milestones - 6 months - movement_physical", "Rolls from tummy to back"),
            ("milestones - 6 months - movement_physical", "Pushes up with straight arms when on tummy"),
        ]

        # Call get_milestone_list
        result = get_milestone_list(kb, "What are the milestones for a 6 month old?")

        # Verify that both items are present under the same category
        self.assertIn("Movement/Physical:", result)
        self.assertIn("- Rolls from tummy to back", result)
        self.assertIn("- Pushes up with straight arms when on tummy", result)

        # Verify that there is only one "Movement/Physical" header
        self.assertEqual(result.count("Movement/Physical:"), 1)

###########################################
### Entry point of test_list_service.py ###
###########################################
if __name__ == "__main__":
    unittest.main()
