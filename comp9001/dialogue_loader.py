import random

class DialogueLoader:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.dialogues = [line.strip() for line in f if line.strip()]
    
    def get_random_dialogue(self):
        return random.choice(self.dialogues) if self.dialogues else "..."
