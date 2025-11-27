# File: test_kb_loader.py
# Author: William Jahner

import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from app.services.kb_loader import load_knowledge_base

######################################################################
# Class: KBLoaderTests
# Description: This class is for testing kb_loader.py functionalities.
######################################################################
class KBLoaderTests(unittest.TestCase):

    ######################################################################
    # Module: setUp
    # Description: A special method used to prepare the test environment
    #              before each test method runs.
    ######################################################################
    def setUp(self):
        # Create a temporary directory and JSON file for each test
        self.temp_dir = TemporaryDirectory()
        self.test_json_path = Path(self.temp_dir.name) / "test_knowledge_base.json"

    ######################################################################
    # Module: tearDown
    # Description: A special method used to clean up the test environment
    #              after each test method runs.
    ######################################################################
    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    ######################################################################
    # Module: write_json
    # Description: A helper function that writes test JSON data to the
    #              temporary file.
    ######################################################################
    def write_json(self, data):
        with open(self.test_json_path, "w") as f:
            json.dump(data, f)

    ######################################################################
    # Module: test_custom_path_argument
    # Description: Tests that pointing to a custom knowledge base path
    #              loads correctly.
    ######################################################################
    def test_custom_path_argument(self):
        # Set up a simple knowledge base in a custom path
        data = {
            "feeding": {
                "6 months": [
                    "Introduce solids",
                    "Continue milk"
                ]
            }
        }
        self.write_json(data)

        # Call load_knowledge_base with the custom path
        result = load_knowledge_base(self.test_json_path)

        # Verify the output
        expected = [
            ("feeding - 6 months", "Introduce solids"),
            ("feeding - 6 months", "Continue milk"),
        ]
        self.assertEqual(sorted(result), sorted(expected))
    
    ######################################################################
    # Module: test_load_simple_list_category
    # Description: Tests that simple list categories are flattened
    #              correctly.
    ######################################################################
    def test_load_simple_list_category(self):
        # Set up a simple list category as seen in the baby_knowledge.json
        data = {
            "sleeping": {
                "newborn": [
                    "Sleeps 14 to 17 hours a day",
                    "Has 45 to 60 minute wake windows"
                ]
            }
        }
        self.write_json(data)

        # Call load_knowledge_base to receive a simple list of tuples
        result = load_knowledge_base(self.test_json_path)

        # Verify the output
        self.assertEqual(len(result), 2)
        self.assertIn(("sleeping - newborn", "Sleeps 14 to 17 hours a day"), result)
        self.assertIn(("sleeping - newborn", "Has 45 to 60 minute wake windows"), result)

    ######################################################################
    # Module: test_load_nested_categories
    # Description: Tests that nested categories are flattened correctly.
    ######################################################################
    def test_load_nested_categories(self):
        # Set up a nested category as seen in the baby_knowledge.json
        data = {
            "milestones": {
                "4 months": {
                    "social_emotional": [
                        "Smiles on their own",
                        "Tries to get your attention"
                    ],
                    "movement_physical": [
                        "Brings hands to mouth"
                    ]
                }
            }
        }
        self.write_json(data)

        # Call load_knowledge_base to receive a nested list of tuples
        result = load_knowledge_base(self.test_json_path)

        # Verify the output
        expected = [
            ("milestones - 4 months - social_emotional", "Smiles on their own"),
            ("milestones - 4 months - social_emotional", "Tries to get your attention"),
            ("milestones - 4 months - movement_physical", "Brings hands to mouth"),
        ]
        self.assertEqual(sorted(result), sorted(expected))

    ######################################################################
    # Module: test_load_mixed_structure
    # Description: Tests that simple list categories and nested categories
    #              both work together.
    ######################################################################
    def test_load_mixed_structure(self):
        # Set up a mixed structure with both simple lists and nested categories
        data = {
            "sleeping": {
                "5 to 6 months": [
                    "sleeps about 13 to 15 hours per day"
                ],
                "10 to 12 months": {
                    "naps": [
                        "2 naps per day"
                    ],
                    "awake_windows": [
                        "3 to 4 hour wake windows"
                    ]
                }
            }
        }
        self.write_json(data)

        # Call load_knowledge_base to receive a mixed list of tuples
        result = load_knowledge_base(self.test_json_path)

        # Verify the output
        expected = [
            ("sleeping - 5 to 6 months", "sleeps about 13 to 15 hours per day"),
            ("sleeping - 10 to 12 months - naps", "2 naps per day"),
            ("sleeping - 10 to 12 months - awake_windows", "3 to 4 hour wake windows"),
        ]
        self.assertEqual(sorted(result), sorted(expected))

########################################
### Entry point of test_kb_loader.py ###
########################################
if __name__ == "__main__":
    unittest.main()
