import tkinter as tk
import random
import os
import pygame
from ui_components import init_ui
from emotion_manager import EmotionManager
from PIL import Image, ImageTk
from effects import apply_text_effect
from shake_effect import trigger_shake_effect
from text_glitch_effects import apply_text_glitch_effect
from new_phase import init_new_phase, handle_new_phase_click

os.chdir(os.path.dirname(os.path.abspath(__file__)))

floating_texts = []
dark_overlay_items = []
file_list_items = []  
file_list_box = None
file_list_close_btn = None

with open("dialogue.txt", "r", encoding="utf-8") as f:
    dialogues = [line.strip() for line in f if line.strip()]
with open("jlm0.txt", "r", encoding="utf-8") as f:
    zero_dialogues = [line.strip() for line in f if line.strip()]

root = tk.Tk()
root.title("comp9001")
root.geometry("580x500")
root.configure(bg="white")

pygame.mixer.init()
pygame.mixer.music.load("assets/FurElise.mp3")  
pygame.mixer.music.set_volume(0.5)         
pygame.mixer.music.play(-1)  

canvas, character, character_img, dialogue_text, change_button = init_ui(root)
emotion_manager = EmotionManager("assets")

is_glitch_active = False
glitch_items = []
click_count = 0
button_click_count = 0
expression_button_click_count = 0
in_zero_mode = False
in_new_phase = False

readme_btn = tk.Button(root, text="readme")
sysfile_btn = tk.Button(root, text="Read system files", command=lambda: show_file_list())
readme_btn.place_forget()
sysfile_btn.place_forget()

test_btn = tk.Button(root, text="NULL", command=lambda: on_special_button_click())
test1_btn = tk.Button(root, text="N U L L", command=lambda: on_special_button_click())
test_btn.place_forget()
test1_btn.place_forget()

def change_character_emotion():
    global expression_button_click_count
    expression_button_click_count += 1

    if expression_button_click_count > 10:
        trigger_shake_effect(canvas)
    else:
        new_image = emotion_manager.get_next_emotion()
        canvas.itemconfig(character, image=new_image)
        canvas.image = new_image

change_button.config(command=change_character_emotion)

def trigger_glitch():
    global is_glitch_active
    is_glitch_active = True
    black_overlay = canvas.create_rectangle(0, 0, 600, 500, fill="black", stipple="gray50")
    glitch_items.append(black_overlay)
    for _ in range(120):
        y = random.randint(0, 500)
        color = random.choice(["#ff00ff", "#00ffff", "#ffff00", "#ff0000"])
        line = canvas.create_line(0, y, 600, y, fill=color, width=2)
        glitch_items.append(line)

def animate_floating_text(text_id, steps=40, dy=-2, delay=30):
    def move_step(step):
        if step >= steps:
            canvas.delete(text_id)
        else:
            canvas.move(text_id, 0, dy)
            root.after(delay, move_step, step + 1)
    move_step(0)

def on_special_button_click():
    global button_click_count, current_display_image

    if in_zero_mode:
        return

    button_click_count += 1

    darkness = canvas.create_rectangle(0, 0, 600, 500, fill="black", stipple="gray50")
    dark_overlay_items.append(darkness)

    text = random.choice(zero_dialogues)
    x = random.randint(30, 320)
    y = random.randint(50, 300)
    font_size = random.randint(10, 48)
    color = random.choice(["red", "black", "white"])

    text_id = canvas.create_text(x, y, text=text, fill=color, font=("Helvetica", font_size, "bold"))
    floating_texts.append(text_id)
    animate_floating_text(text_id)

    if button_click_count >= 10:
        enter_zero_mode()

def on_character_click(event=None):
    global is_glitch_active, glitch_items, click_count, in_zero_mode, in_new_phase

    if is_glitch_active:
        for item in glitch_items:
            canvas.delete(item)
        glitch_items.clear()
        is_glitch_active = False
        return

    if in_zero_mode:
        restore_normal_state()
        return

    if in_new_phase:
        handle_new_phase_click(canvas, character, dialogue_text)
        return

    selected_line = random.choice(dialogues)
    char_x, char_y = canvas.coords(character)

    apply_text_effect(
        canvas,
        dialogue_text,
        (char_x, char_y),
        selected_line,
        default_font=("Helvetica", 14),
        on_complete=lambda: apply_text_glitch_effect(
            canvas,
            dialogue_text,
            selected_line,
            (char_x, char_y),
            default_font=("Helvetica", 14)
        )
    )

    click_count += 1
    if click_count > 10:
        test_btn.place(x=200, y=220)
        test1_btn.place(x=280, y=220)

    if click_count >= 15 and not in_new_phase:
        enter_new_phase()

    if random.random() < 0.1:
        trigger_glitch()

def enter_zero_mode():
    global in_zero_mode, current_display_image
    in_zero_mode = True

    test_btn.place_forget()
    test1_btn.place_forget()

    trigger_glitch()

    pil_img = Image.open("assets/0.png")
    current_display_image = ImageTk.PhotoImage(pil_img)
    canvas.itemconfig(character, image=current_display_image)
    canvas.image = current_display_image

    canvas.itemconfig(dialogue_text, text=random.choice(zero_dialogues))

def restore_normal_state():
    global click_count, button_click_count, in_zero_mode, expression_button_click_count
    click_count = 0
    button_click_count = 0
    expression_button_click_count = 0
    in_zero_mode = False

    for item in floating_texts:
        canvas.delete(item)
    floating_texts.clear()

    for overlay in dark_overlay_items:
        canvas.delete(overlay)
    dark_overlay_items.clear()

    canvas.itemconfig(dialogue_text, text=random.choice(dialogues))
    change_character_emotion()

def enter_new_phase():
    global in_new_phase
    in_new_phase = True
    readme_btn.place(x=400, y=200)
    sysfile_btn.place(x=400, y=250)
    init_new_phase(canvas, character)
    change_button.config(state="disabled") 


def show_file_list():
    global file_list_box, file_list_items, file_list_close_btn
    canvas.itemconfig(dialogue_text, text="")  

    file_list_box = canvas.create_rectangle(50, 50, 530, 400, fill="black", stipple="gray50")
    file_list_items.append(file_list_box)

    x_button = tk.Button(root, text="X", command=close_file_list, bg="gray", fg="white")
    x_button.place(x=55, y=55)
    file_list_close_btn = x_button

    files = os.listdir(".")
    for i, filename in enumerate(files):
        text = canvas.create_text(70, 80 + i * 20, anchor="nw", text=filename, fill="white", font=("Helvetica", 10))
        file_list_items.append(text)

def close_file_list():
    global file_list_items, file_list_box, file_list_close_btn
    for item in file_list_items:
        canvas.delete(item)
    file_list_items.clear()

    if file_list_close_btn:
        file_list_close_btn.destroy()
        file_list_close_btn = None

    canvas.itemconfig(dialogue_text, text=random.choice(dialogues))

canvas.bind("<Button-1>", on_character_click)
on_character_click()
root.mainloop()
