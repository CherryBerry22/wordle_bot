import os
import pyautogui as ag
from PIL import Image

# find a pixel in the top left letter
FIRST_LETTER = 580
INITIAL_ROW = 470
# distance to same spot in next letter
OFFSET = 170

def get_colors(guess_num):
    ag.screenshot('current_screen.jpg')
    img = Image.open('current_screen.jpg')
    pix = img.load()
    guess_row = INITIAL_ROW + (OFFSET * (guess_num-1))
    colors = []
    for i in range(0, 5):
        color = pix[FIRST_LETTER + OFFSET * i, guess_row]
        if color == (107, 170, 100):
            colors.append('g')
        elif color == (201, 180, 89):
            colors.append('y')
        else:
            colors.append('n')

    print(colors)
    os.remove("current_screen.jpg")
    return colors

# for my screen starts at x=550 y=485
# each box is 155x155 with 15px gap between letters and rows
def mouse_pos():
    while True:
        print(ag.position())
        ag.screenshot('current_screen.jpg')
        img = Image.open('current_screen.jpg')
        pix = img.load()


