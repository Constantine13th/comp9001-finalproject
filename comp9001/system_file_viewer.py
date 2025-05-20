import os
from tkinter import Canvas

system_view_items = []

def show_file_view(canvas, dialogue_text):
    dialogue_text.place_forget()  

    black_box = canvas.create_rectangle(50, 100, 530, 400, fill="black", stipple="gray50")
    system_view_items.append(black_box)

    filenames = os.listdir(".")
    text_content = "\n".join(filenames)

    text_id = canvas.create_text(60, 120, anchor="nw", text=text_content, fill="white", font=("Consolas", 10), width=460)
    system_view_items.append(text_id)

    close_btn = canvas.create_text(55, 105, text="X", fill="red", font=("Arial", 14, "bold"))
    system_view_items.append(close_btn)

    def close_view(event=None):
        for item in system_view_items:
            canvas.delete(item)
        system_view_items.clear()
        dialogue_text.place(x=30, y=420) 

    canvas.tag_bind(close_btn, "<Button-1>", close_view)
