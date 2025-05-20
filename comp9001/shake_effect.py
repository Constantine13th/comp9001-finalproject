import os 
import random
from PIL import Image, ImageTk, ImageOps

shake_offset_range = 10
shake_speed = 30

shake_images = []
shake_character_ids = []
shake_background_ids = []
shake_running = False
top_tk_images = []

def pixelate(img, factor=8):
    small = img.resize((max(1, img.width // factor), max(1, img.height // factor)), resample=Image.BILINEAR)
    return small.resize(img.size, Image.NEAREST)

def trigger_shake_effect(canvas):
    global shake_images, shake_character_ids, shake_running, top_tk_images, shake_background_ids

    if shake_running:
        return
    shake_running = True
    shake_images.clear()
    shake_character_ids.clear()
    shake_background_ids.clear()
    top_tk_images.clear()

    def load_and_place(image_name, x=290, y=250, apply_pixelate=False):
        img = Image.open(f"assets/{image_name}")
        if apply_pixelate:
            img = pixelate(img, factor=8)
        tk_img = ImageTk.PhotoImage(img)
        img_id = canvas.create_image(x, y, image=tk_img)
        top_tk_images.append(tk_img)
        shake_character_ids.append(img_id)
        return img_id, img

    # === jlmtest.png 马赛克图像 ===
    load_and_place("jlmtest.png", apply_pixelate=True)

    # === jlmtest2.png 黑白切换闪烁用 ===
    img_id, img_color = load_and_place("jlmtest2.png", x=270, y=270)
    img_bw = ImageOps.grayscale(img_color).convert("RGB")
    tk_color = ImageTk.PhotoImage(img_color)
    tk_bw = ImageTk.PhotoImage(img_bw)
    top_tk_images.extend([tk_color, tk_bw])

    def toggle_bw(step=0):
        if step > 100:
            return
        canvas.itemconfig(img_id, image=tk_color if step % 2 == 0 else tk_bw)
        canvas.after(100, lambda: toggle_bw(step + 1))

    toggle_bw()

    load_and_place("jlmtest3.png", x=310, y=230)

    all_files = os.listdir("assets")
    image_files = [f for f in all_files if f.endswith(".png")]
    exclude = ["jlmtest.png", "jlmtest2.png", "jlmtest3.png"]
    image_files = [f for f in image_files if f not in exclude]

    selected_bg = random.sample(image_files, min(5, len(image_files)))
    directions = [
        lambda: (random.randint(0, 600), 0),     
        lambda: (random.randint(0, 600), 500),  
        lambda: (0, random.randint(0, 500)),    
        lambda: (600, random.randint(0, 500)),   
        lambda: (random.randint(0, 600), random.randint(0, 500))  
    ]
    random.shuffle(directions)

    for i, filename in enumerate(selected_bg):
        img = Image.open(os.path.join("assets", filename))
        scale = random.uniform(0.4, 0.7)
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size)
        tk_img = ImageTk.PhotoImage(img)
        x, y = directions[i % len(directions)]()
        img_id = canvas.create_image(x, y, image=tk_img)
        top_tk_images.append(tk_img)
        shake_background_ids.append(img_id)


    selected_fg = random.sample(image_files, min(5, len(image_files)))
    for filename in selected_fg:
        img = Image.open(os.path.join("assets", filename))
        tk_img = ImageTk.PhotoImage(img)
        x = random.randint(50, 500)
        y = random.randint(50, 400)
        img_id = canvas.create_image(x, y, image=tk_img)
        top_tk_images.append(tk_img)
        shake_images.append((img_id, tk_img))

    for img_id in shake_character_ids:
        canvas.tag_raise(img_id)

    def shake(step=0):
        if step > 30:
            return
        for img_id in shake_character_ids:
            dx = random.randint(-shake_offset_range, shake_offset_range)
            dy = random.randint(-shake_offset_range, shake_offset_range)
            canvas.move(img_id, dx, dy)
        canvas.after(shake_speed, lambda: shake(step + 1))

    shake()

    def cleanup():
        global shake_running
        for img_id, _ in shake_images:
            canvas.delete(img_id)
        for img_id in shake_character_ids:
            canvas.delete(img_id)
        for img_id in shake_background_ids:
            canvas.delete(img_id)
        shake_images.clear()
        shake_character_ids.clear()
        shake_background_ids.clear()
        top_tk_images.clear()
        shake_running = False

    canvas.after(5000, cleanup)
