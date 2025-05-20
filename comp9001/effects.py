import random
import tkinter as tk

def apply_text_effect(canvas, dialogue_text_item, character_coords, text, default_font=("Helvetica", 14), on_complete=None):

    if random.random() > 0.3:

        if on_complete:
            on_complete()
        return

    original_text = canvas.itemcget(dialogue_text_item, "text")
    original_font = canvas.itemcget(dialogue_text_item, "font")
    original_fill = canvas.itemcget(dialogue_text_item, "fill")

    char_x, char_y = character_coords


    big_font = ("Helvetica", 50, "bold")
    temp_text = canvas.create_text(char_x, char_y, text=text, fill="red", font=big_font)

    def shake(count=0):
        if count >= 8:
            canvas.delete(temp_text)
            canvas.itemconfig(dialogue_text_item, text=text, font=default_font, fill="black")
            if on_complete:
                on_complete()
            return
        dx = (-1) ** count * 3 
        canvas.move(temp_text, dx, 0)
        canvas.after(50, shake, count + 1)

    shake()

