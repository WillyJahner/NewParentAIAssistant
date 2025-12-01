# File: test_main.py
# Author: William Jahner

import unittest
from unittest.mock import patch, MagicMock
import torch
from app.main import NewParentAIAssistantApp, print_intro_message

######################################################################
# Class: MainTests
# Description: This class is for testing main.py functionalities.
######################################################################
class MainTests(unittest.TestCase):

    ######################################################################
    # Module: setUp
    # Description: A special method used to prepare the test environment
    #              before each test method runs.
    ######################################################################
    def setUp(self):
        # Create a simple fake knowledge base and app instance for reuse
        self.fake_kb = [
            ("milestones", "Babies reach various milestones as they grow."),
            ("feeding", "Breastfeeding is recommended for the first 6 months."),
            ("sleep", "As babies grow, their sleep patterns change."),
        ]

        # Create app (note that AI internals will be mocked)
        self.app = NewParentAIAssistantApp(self.fake_kb)

    ######################################################################
    # Module: test_print_intro_message
    # Description: Tests that the introductory message prints correctly.
    ######################################################################
    def test_print_intro_message(self):
        # Ensure the intro message prints the expected text.
        with patch("builtins.print") as mock_print:
            print_intro_message()

            mock_print.assert_any_call("\nWelcome to the New Parent AI Assistant!")
            mock_print.assert_any_call("This application is designed to help answer questions for new parents.")
            mock_print.assert_any_call("This is the initial version of the application, so it only contains information " + \
                                       "about developmental milestones, feeding, and sleep for babies in their first year.")
            mock_print.assert_any_call("Future releases of this application will include more categories of baby care.")
            mock_print.assert_any_call("If you wish to end the program at any time, enter 'exit', 'end', or 'quit'\n\n")

    ######################################################################
    # Module: test_find_best_entries
    # Description: Tests that the function find_best_entries returns top
    #              entries based on mocked scores.
    ######################################################################
    @patch("app.main.util")
    def test_find_best_entries(self, mock_util):        
        # Mock embedder.encode on the embedded AI service
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = torch.tensor([1, 1, 1])

        # Replace the real embedder with our mock
        self.app.ai.embedder = mock_embedder

        # Mock cosine similarity scores
        # (higher score → more relevant)
        mock_util.pytorch_cos_sim.return_value = torch.tensor([[0.7, 0.2, 0.9]])

        # Run function
        results = self.app.find_best_entries("Do babies sleep differently than adults?", top_k=2)

        # Expected order: index 3 (0.9) then index 1 (0.7)
        expected = [
            "sleep: As babies grow, their sleep patterns change.",
            "milestones: Babies reach various milestones as they grow.",
        ]

        self.assertEqual(results, expected)

    ######################################################################
    # Module: test_answer_question
    # Description: Tests the function answer_question using fully mocked
    #              dependencies.
    ######################################################################
    def test_answer_question(self):        
        # Patch find_best_entries to avoid testing it again here
        with patch.object(self.app, "find_best_entries", return_value=["context1", "context2"]):
            # Mock the QA model response
            mock_qa = MagicMock()
            mock_qa.return_value = {"answer": "Mocked answer"}

            # Replace the real QA pipeline with our mock
            self.app.ai.qa_pipeline = mock_qa

            # Call the tested function (answer_question)
            answer = self.app.answer_question("test question")

            # Ensure the QA model is called correctly
            mock_qa.assert_called_once_with(question="test question", context="context1 context2")

            # Check the returned answer
            self.assertEqual(answer, "Mocked answer")

###################################
### Entry point of test_main.py ###
###################################
if __name__ == "__main__":
    unittest.main()
