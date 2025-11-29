# File: test_ai_service.py
# Author: William Jahner

import unittest
from unittest.mock import patch, MagicMock
from app.services.ai_service import AIService

######################################################################
# Class: TestAIService
# Description: This class is for testing ai_service.py functionalities.
######################################################################
class TestAIService(unittest.TestCase):

    ######################################################################
    # Module: test_init_loads_models
    # Description: Tests that the models load during initialization.
    ######################################################################
    @patch("app.services.ai_service.SentenceTransformer")
    @patch("app.services.ai_service.pipeline")
    def test_init_loads_models(self, mock_pipeline, mock_embedder):
        # Mock qa_pipeline and embedder
        mock_pipeline.return_value = MagicMock(name="mock_qa_pipeline")
        mock_embedder.return_value = MagicMock(name="mock_embedder")

        # Create a new AIService
        service = AIService("test context")

        # Verify the models load correctly
        mock_pipeline.assert_called_once_with("question-answering", model="deepset/roberta-base-squad2")
        mock_embedder.assert_called_once_with("all-MiniLM-L6-v2")
        self.assertEqual(service.context, "test context")

    ######################################################################
    # Module: test_ask_question_success
    # Description: Tests that a call to ask_question returns an answer
    #              when the pipeline works.
    ######################################################################
    @patch("app.services.ai_service.SentenceTransformer")
    @patch("app.services.ai_service.pipeline")
    def test_ask_question_success(self, mock_pipeline, mock_embedder):
        # Mock qa_pipeline and embedder
        mock_pipeline.return_value = MagicMock(name="qa_mock")
        mock_embedder.return_value = MagicMock()

        # Create a new AIService
        service = AIService("test context")

        # Mock the return value for qa_pipeline
        service.qa_pipeline = MagicMock()
        service.qa_pipeline.return_value = {
            "answer": "The baby should nap 3 times a day."
        }

        # Call AIService ask_question method
        answer = service.ask_question("How often should my 5 month old baby nap?")

        # Verify the call and returned answer
        service.qa_pipeline.assert_called_once_with(
            question="How often should my 5 month old baby nap?",
            context="test context"
        )
        self.assertEqual(answer, "The baby should nap 3 times a day.")

    ######################################################################
    # Module: test_ask_question_exception
    # Description: Tests that a call to ask_question returns a friendly
    #              error message when the pipeline fails.
    ######################################################################
    @patch("app.services.ai_service.SentenceTransformer")
    @patch("app.services.ai_service.pipeline")
    def test_ask_question_exception(self, mock_pipeline, mock_embedder):
        # Mock qa_pipeline and embedder
        mock_pipeline.return_value = MagicMock()
        mock_embedder.return_value = MagicMock()

        # Create a new AIService
        service = AIService("test context")

        # Mock the qa_pipeline to result in a runtime error
        service.qa_pipeline = MagicMock()
        service.qa_pipeline.side_effect = RuntimeError("Model failure")

        # Call AIService ask_question method
        answer = service.ask_question("What do babies eat?")

        # Verify the error message returned
        self.assertIn("Sorry, the answer could not be determined.", answer)
        self.assertIn("Model failure", answer)

####################################
### Entry point of ai_service.py ###
####################################
if __name__ == "__main__":
    unittest.main()
