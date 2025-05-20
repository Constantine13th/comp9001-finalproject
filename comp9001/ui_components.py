import tkinter as tk

def init_ui(root):
    canvas = tk.Canvas(root, width=600, height=500, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    image = tk.PhotoImage(file="assets/jlm_1.png")
    character = canvas.create_image(300, 200, image=image)

    # 半透明灰色对话框（使用 stipple 实现透明度）
    dialogue_box = canvas.create_rectangle(
        50, 400, 550, 475, fill="white", outline="gray", width=2
    )
    canvas.itemconfig(dialogue_box, stipple="gray50")

    # 对话文字
    dialogue_text = canvas.create_text(
        60, 415, anchor='nw', text="", fill="white", font=("Arial", 12), width=480
    )

    # 更换表情按钮（预留）
    change_button = tk.Button(root, text="Change Emotion")
    change_button.place(x=480, y=20)

    return canvas, character, image, dialogue_text, change_button
