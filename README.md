# comp9001-finalproject

This is a game designed in the style of a galgame interface, featuring elements such as jump scares, META mechanics, and anime-style character illustrations.

*Programming Language*: Python

*Character Illustrations*: Custom commissioned and paid assets

*Background Music*: Für Elise

### How to Play

Run the game using:

```python main.py```

Click the screen to progress through dialogue.
In the first phase, the Change Emotion button is used to switch the character’s facial expressions. After repeatedly clicking it multiple times, special buttons will appear. Clicking these buttons will generate floating text with random colors, fonts, and content.

After 10 clicks, a black screen will be triggered, the character image will change, and special text will be displayed. Clicking the character again will restore the initial state and clear all floating text and the blackout effect.

Once the character is clicked more than 15 times, the game enters Phase Two, where two new buttons appear: readme (non-clickable) and Read System Files. At this point, the character will automatically disable the emotion switching function. Clicking Read System Files will open a black window listing all files in the current directory.

**Demo video**

https://github.com/Constantine13th/comp9001-finalproject/blob/main/img/demo.mp4

******The jump scare is triggered by clicking the emotion switch button 10 times in a row.******

**Character Art Preview**

![ ](/img/readme1.png)

**Interface Previews**

![ ](/img/readme2.png)
![ ](/img/readm3.png)
![ ](/img/readme4.png)
![ ](/img/readme5.png)
![ ](/img/readme6.png)

### File Descriptions

*assets*— Folder containing image and sound resources

*0.txt, jlm0.txt, newdialogue.txt* — Text content files

*ui_components.py* — UI construction module for the initial phase, includes dialogue boxes, buttons, and image frames

*newui_components.py* — UI module used by new_phase.py, featuring a more system-like style with a white background and black text

*system_file_viewer.py* — Module responsible for displaying system files in a pop-up window

*effects.py* — Base visual effects module (black screen, floating text, slide-in display)

*shake_effect.py* — Module for high-frequency shake and top-layer image overlay effects; triggers jlmtest.png and randomly loads five images

*text_glitch_effects.py* — Text glitch effects including pseudo-garble insertion, garble flash, and multi-layer offset floating text

*main.py* — Main game logic file

*new_phase.py* — Controls the new storyline phase; replaces the main logic when entering the new chapter and handles pseudo-code display, simulated system behaviors, and input disabling

*dialogue_loader.py* — Dialogue text loader

*emotion_manager.py* — Manages character expressions by loading and cycling through images in the assets folder







