import os
from itertools import cycle
from tkinter import PhotoImage

class EmotionManager:
    def __init__(self, asset_dir, prefix='jlm_'):
      
        self.images = [
            PhotoImage(file=os.path.join(asset_dir, f))
            for f in sorted(os.listdir(asset_dir))
            if f.startswith(prefix) and f.endswith('.png')
        ]
        self.cycle = cycle(self.images)
    
    def get_next_emotion(self):
        return next(self.cycle)
