import os
import random
from PIL import Image, ImageTk
from newui_components import create_new_ui

allowed_emotions = ["jlm_3.png", "jlm_4.png", "jlm_5.png"]
new_dialogue_index = 0
new_dialogues = []

system_frame = None
system_text_items = []
close_button_id = None
system_mode_active = False
system_simulating = False
code_simulating = False  


def init_new_phase(canvas, character):
    global new_dialogues
    with open("newdialogue.txt", "r", encoding="utf-8") as f:
        new_dialogues = [line.strip() for line in f if line.strip()]


    img_path = f"assets/{random.choice(allowed_emotions)}"
    img = Image.open(img_path)
    tk_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(character, image=tk_img)
    canvas.image = tk_img


    dialogue_box, dialogue_text = create_new_ui(canvas)
    canvas.tag_lower(dialogue_box)
    canvas.tag_raise(dialogue_text)
    canvas.coords(dialogue_box, 50, 400, 550, 475)
    canvas.coords(dialogue_text, 60, 415)
    canvas.itemconfig(dialogue_text, fill="white")

    return dialogue_box, dialogue_text


def handle_new_phase_click(canvas, character, dialogue_text):
    global new_dialogue_index, new_dialogues, system_simulating, code_simulating

    if system_simulating or code_simulating:
        return

    if not new_dialogues:
        return

    current_line = new_dialogues[new_dialogue_index]

    if new_dialogue_index == 4:
        simulate_system_behavior(canvas, dialogue_text)
        new_dialogue_index += 1
        return

    if new_dialogue_index == 6:
        simulate_code_display(canvas, dialogue_text)
        new_dialogue_index += 1
        return

    canvas.itemconfig(dialogue_text, text=current_line, fill="black")

    img_path = f"assets/{random.choice(allowed_emotions)}"
    img = Image.open(img_path)
    tk_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(character, image=tk_img)
    canvas.image = tk_img

    new_dialogue_index = (new_dialogue_index + 1) % len(new_dialogues)


def simulate_system_behavior(canvas, dialogue_text):
    global system_simulating, system_text_items
    system_simulating = True
    canvas.itemconfig(dialogue_text, text="")

    lines = [
        "username = get_current_username()",
        "Current user: {???????}",
        '⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️',
        '#Current character file does not match the hash value of ????.chr',
        'show_dialogue("Access denied.")',
        'show_dialogue("Insufficient privileges.")'
    ]

    display_lines(canvas, lines, dialogue_text, color="red", on_finish=lambda: finish_simulation(canvas, dialogue_text))

def simulate_code_display(canvas, dialogue_text):
    global code_simulating, system_text_items
    code_simulating = True
    canvas.itemconfig(dialogue_text, text="")

    code_lines = [
        "for name in ['hello', ' ?', 'test']:",
        "    tk.Button(root, text=name).pack()",
        "root.mainloop()"
    ]

    display_lines(canvas, code_lines, dialogue_text, color="blue", on_finish=lambda: finish_code_simulation(canvas, dialogue_text))

def display_lines(canvas, lines, dialogue_text, index=0, color="red", on_finish=None):
    global system_text_items

    if index >= len(lines):
        if on_finish:
            canvas.after(1000, on_finish)
        return

    y = 150 + index * 30
    text_item = canvas.create_text(50, y, text="", fill=color, font=("Consolas", 12), anchor="nw")
    system_text_items.append(text_item)

    def type_characters(i=0):
        if i <= len(lines[index]):
            canvas.itemconfig(text_item, text=lines[index][:i])
            canvas.after(50, lambda: type_characters(i + 1))
        else:
            canvas.after(300, lambda: display_lines(canvas, lines, dialogue_text, index + 1, color, on_finish))

    type_characters()

def finish_simulation(canvas, dialogue_text):
    global system_simulating, system_text_items
    for item in system_text_items:
        canvas.delete(item)
    system_text_items.clear()
    system_simulating = False
    canvas.itemconfig(dialogue_text, fill="black", text="...")

def finish_code_simulation(canvas, dialogue_text):
    global code_simulating, system_text_items
    for item in system_text_items:
        canvas.delete(item)
    system_text_items.clear()
    code_simulating = False
    canvas.itemconfig(dialogue_text, fill="black", text="...")

def show_system_files(canvas, dialogue_text):
    global system_frame, system_text_items, close_button_id, system_mode_active

    if system_mode_active:
        return
    system_mode_active = True

    canvas.itemconfig(dialogue_text, text="")
    system_frame = canvas.create_rectangle(30, 100, 550, 400, fill="black", stipple="gray50")

    files = os.listdir(".")
    for i, filename in enumerate(files):
        item = canvas.create_text(50, 120 + i * 20, text=filename, anchor="nw", fill="white", font=("Helvetica", 12))
        system_text_items.append(item)

    close_button_id = canvas.create_text(40, 105, text="X", fill="red", font=("Helvetica", 14, "bold"), anchor="nw")
    canvas.tag_bind(close_button_id, "<Button-1>", lambda e: close_system_view(canvas, dialogue_text))


def close_system_view(canvas, dialogue_text):
    global system_frame, system_text_items, close_button_id, system_mode_active

    if system_frame:
        canvas.delete(system_frame)
        system_frame = None
    for item in system_text_items:
        canvas.delete(item)
    system_text_items.clear()

    if close_button_id:
        canvas.delete(close_button_id)
        close_button_id = None

    canvas.itemconfig(dialogue_text, text="", fill="black")
    system_mode_active = False
