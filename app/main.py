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

    questions = [
        "When can my baby start solid foods?",
        "How often should a newborn eat?",
        "What should a 3 month old baby be able to do?"
    ]

    for q in questions:
        print(f"Q: {q}")
        print(f"A: {new_parent_assistant.ask(q)}\n")
 