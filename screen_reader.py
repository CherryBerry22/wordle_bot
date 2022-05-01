import os
import pyautogui as ag
from PIL import Image
from pynput import mouse

# find a pixel in the top left letter
FIRST_LETTER = 580
INITIAL_ROW = 500
# distance to same spot in next letter
OFFSET = 170
class ScreenReader:

    def __init__(self):
        skip = input("enter s to skip setup")
        if skip == 's':
            self.initial_row = INITIAL_ROW
            self.first_letter = FIRST_LETTER
            self.offset = OFFSET
        else:
            self.click_counter = 0
            listener = mouse.Listener(
                on_click=self.on_click)
            listener.start()
            input('please click in top left square and next square to set initial pos and offset then press enter')
            listener.stop()

    def on_click(self, x, y, button, pressed):
        if self.click_counter == 0:
            self.click_counter += 1
            self.initial_row = y
            self.first_letter = x
            print('first square set to {0},{1}'.format(x, y))
        elif self.click_counter == 1:
            self.click_counter += 1
        elif self.click_counter == 2:
            self.click_counter += 1
            self.offset = y - self.initial_row
            print('offset set to {0}'.format(self.offset))
        else:
            pass

    def get_colors(self, guess_num):
        ag.screenshot('current_screen.jpg')
        img = Image.open('current_screen.jpg')
        pix = img.load()
        guess_row = INITIAL_ROW + (OFFSET * (guess_num-1))
        colors = []
        for i in range(0, 5):
            color = pix[FIRST_LETTER + OFFSET * i, guess_row]
            if 100 <= color[0] <= 110 and \
                    165 <= color[1] <= 175 and\
                    95 <= color[2] <= 105:
                colors.append('g')
            elif 195 <= color[0] <= 205 and \
                    175 <= color[1] <= 185 and\
                    85 <= color[2] <= 95:
                colors.append('y')
            else:
                colors.append('n')

        print(colors)
        os.remove("current_screen.jpg")
        return colors





# for my screen starts at x=550 y=485
# each box is 155x155 with 15px gap between letters and rows
def mouse_pos(x,y):
    print(ag.position())
    ag.screenshot('current_screen.jpg')
    img = Image.open('current_screen.jpg')
    hsv_img = img.convert('HSV')
    pix = img.load()
    hsv_pix = hsv_img.load()
    print('Color at {0},{1}: '
          '\n RGB {2} '
          '\n HSV {3}'
          .format(x, y, pix[x, y], hsv_pix[x, y]))
    os.remove('current_screen.jpg')


