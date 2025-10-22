# File: ai_service.py
# Author: William Jahner

from transformers import pipeline

######################################################################
# Class: AIService
# Description: The class that uses AI logic to answer user questions
######################################################################
class AIService:
    
    ######################################################################
    # Module: __init__
    # Description: Constructor for AIService
    # Input:
    #   - self: instance of the class itself
    #   - context_text: the knowledge base for the NLP model
    # Returns: N/A
    ######################################################################
    def __init__(self, context_text: str):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.context = context_text

    ######################################################################
    # Module: ask_question
    # Description: Returns an answer for a user's question by using the
    #              AI pipeline
    # Input:
    #   - self: instance of the class itself
    #   - question: the user's question
    # Returns: the answer to the user's question
    ######################################################################
    def ask_question(self, question: str) -> str:
        # Try to answer the user's question.
        # If able to answer the user's question, return the answer.
        # Otherwise, return a message to the user noting that the answer could not be determined
        try:
            result = self.qa_pipeline(question=question, context=self.context)
            return result["answer"]
        except Exception as e:
            return f"Sorry, the answer could not be determined. ({e})"
