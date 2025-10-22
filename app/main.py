import json
from transformers import pipeline
from pathlib import Path

def load_knowledge_base(path=Path(__file__).parent.parent / "data/baby_knowledge.json"):
    with open(path, "r") as f:
        data = json.load(f)
    # Flatten into a single context string
    all_entries = []
    for category in data.values():
        for entry in category:
            all_entries.append(entry["description"])
    return " ".join(all_entries)

def print_intro_message():
    print("\nWelcome to the New Parent AI Assistant!")
    print("If you wish to end the program at any time, enter 'exit', 'end', or 'quit'\n\n")

class NewParentAssistant:
    def __init__(self, knowledge_base_text):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.context = knowledge_base_text

    def ask(self, question: str) -> str:
        try:
            result = self.qa_pipeline(question=question, context=self.context)
            return result["answer"]
        except Exception as e:
            return f"Sorry, I couldn’t find an answer. ({e})"

if __name__ == "__main__":
    knowledge_base_text = load_knowledge_base()
    new_parent_assistant = NewParentAssistant(knowledge_base_text)
    print_intro_message()

    # Note that we start running the AI assistant here
    while True:
        user_input = input("What would you like to know?\n").strip().lower()

        if user_input in ("exit", "end", "quit"):
            print("Ending New Parent AI Assistant...")
            break

        print(f"Response: {new_parent_assistant.ask(user_input)}\n")
