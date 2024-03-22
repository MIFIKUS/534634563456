from ahk import AHK
import pyautogui
import time

ahk = AHK()

class Mouse:
    """Класс для работы с мышкой"""
    def __init__(self):
        self.SPEED = 0.5

    def move_and_click(self, x, y):
        """Функция чтобы навестись на координаты на экране и кликнуть на это точку"""
        self.move(x, y)
        self.click()

    def move(self, x, y):
        """Функция чтобы переместить курсор на заданные координаты"""
        pyautogui.moveTo(x, y, self.SPEED)

    def move_instantly(self, x, y):
        """Функция чтобы мгновенно переместить курсор на нужные координаты"""
        pyautogui.moveTo(x, y, 0)


    def click(self):
        """Функция чтобы сделать клик мышкой"""
        pyautogui.click()

    def drag(self, x, y):
        """Функция для того чтобы переместить мышку на нужные координаты с зажатой левой кнопкой"""
        pyautogui.mouseDown(button='left')
        self.move(x, y)
        pyautogui.mouseUp(button='left')

    def scroll_down(self, amount):
        """Функция для того прокрутить колесико мышки вниз\n
        amount - колличество прокруток
        """
        amount *= 100
        pyautogui.scroll(-amount)

    def scroll_up(self, amount):
        """Функция для того что прокрутить колесико мышки вверх
        amount - колличество прокруток
        """
        amount *= 100
        pyautogui.scroll(amount)

class Keyboard:
    def arrow_down(self):
        ahk.run_script('SendInput, {Down}')

    def esc(self):
        ahk.key_press('esc')

    def enter(self):
        ahk.key_press('enter')

    def tab(self):
        pyautogui.press('tab')

    def copy(self):
        pyautogui.hotkey('ctrl', 'c')

    def ctrl_i(self):
        for _ in range(2):
            pyautogui.hotkey('ctrl', 'i')
            time.sleep(0.1)

