import tkinter as tk
import random
import math

GLITCH_CHARS = ['⍰', '␣', '␤', '␦', '⧖', '⧓', '⬛', '█', '▓', '▒', '░', '�']

def apply_text_glitch_effect(canvas, label, original_text, coords, default_font=("Helvetica", 10)):
    if random.random() < 0.2:
        glitched = ""
        for char in original_text:
            glitched += char
            if random.random() < 0.3:
                glitched += random.choice(GLITCH_CHARS)
        canvas.itemconfig(label, text=glitched, fill="black")
        return

    if random.random() < 0.3:
        canvas.itemconfig(label, text="⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛", fill="black")
        canvas.after(900, lambda: canvas.itemconfig(label, text=original_text, fill="black"))  # 停留时间延长
        return

    if random.random() < 0.5:
        for _ in range(random.randint(3, 4)):
            dx = random.randint(-5, 5)
            dy = random.randint(-7, 3)
            angle = random.randint(-20, 30)
            color = random.choice(["red", "blue", "black", "white"])
            text_id = canvas.create_text(
                coords[0] + dx, coords[1] + dy,
                text=original_text,
                fill=color,
                font=default_font
            )
            canvas.after(900, lambda tid=text_id: canvas.delete(tid))  
        canvas.itemconfig(label, text="", fill="black")  
        canvas.after(900, lambda: canvas.itemconfig(label, text=original_text, fill="black")) 
        return

    canvas.itemconfig(label, text=original_text, fill="black")
