# File: main.py
# Author: William Jahner

from sentence_transformers import SentenceTransformer, util
import torch
from services.ai_service import AIService
from services.kb_loader import load_knowledge_base

######################################################################
# Module: print_intro_message
# Description: Prints the introductory message for a user starting up
#              the application
# Input: N/A
# Returns: N/A
######################################################################
def print_intro_message():
    print("\nWelcome to the New Parent AI Assistant!")
    print("If you wish to end the program at any time, enter 'exit', 'end', or 'quit'\n\n")

######################################################################
# Module: find_best_entries
# Description: TODO: helper function...
# Input:
#   - question: TODO
#   - top_k: TODO
# Returns: TODO
######################################################################
def find_best_entries(question, top_k=3):
    # Find the top_k most relevant knowledge base entries to the user's question.
    q_embed = new_parent_ai_assistant.embedder.encode(question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(q_embed, embeddings)[0]
    top_results = torch.topk(scores, k=top_k)
    return [texts[i] for i in top_results.indices]

######################################################################
# Module: answer_question
# Description: TODO: helper function...
# Input:
#   - question: TODO
# Returns: TODO
######################################################################
def answer_question(question):
    # Retrieve relevant info and generate an answer using the QA model.
    top_contexts = find_best_entries(question)
    context = " ".join(top_contexts)
    result = new_parent_ai_assistant.qa_model(question=question, context=context)
    return result["answer"]

#############################################
### Entry point of the application (main) ###
#############################################
if __name__ == "__main__":
    # Load the knowledge base
    knowledge_base_text = load_knowledge_base()

    # Instantiate a new AI Service
    new_parent_ai_assistant = AIService(knowledge_base_text)

    # Create embeddings for each entry
    texts = [f"{label}: {text}" for label, text in knowledge_base_text]
    embeddings = new_parent_ai_assistant.embedder.encode(texts, convert_to_tensor=True)

    # Print the introductory message
    print_intro_message()

    # Run the New Parent AI Assistant application
    # Note that the application runs until the user enters an escape keyword
    while True:
        # Prompt the user to ask a question and save the user's input
        user_input = input("What would you like to know?\n").strip().lower()

        # If the user enters 'exit', 'end', or 'quit', exit the application
        if user_input in ("exit", "end", "quit"):
            print("Closing the New Parent AI Assistant...")
            break

        # Print the response to the user's question
        print(f"NLP RESPONSE: {answer_question(user_input)}\n")
        #print(f"Response: {new_parent_ai_assistant.ask_question(user_input)}\n")
