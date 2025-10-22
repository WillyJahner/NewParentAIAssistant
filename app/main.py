# File: main.py
# Author: William Jahner

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

#############################################
### Entry point of the application (main) ###
#############################################
if __name__ == "__main__":
    # Load the knowledge base
    knowledge_base_text = load_knowledge_base()

    # Instantiate a new AI Service
    new_parent_ai_assistant = AIService(knowledge_base_text)

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
        print(f"Response: {new_parent_ai_assistant.ask_question(user_input)}\n")
