# newui_components.py
def create_new_ui(canvas):

    dialogue_box = canvas.create_rectangle(50, 450, 600, 475, fill="white", outline="black", width=2)
    
  
    dialogue_text = canvas.create_text(60, 415, text="", fill="black", font=("Helvetica", 12), anchor="nw")
    
    return dialogue_box, dialogue_text
