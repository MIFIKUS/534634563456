from ahk import AHK
import pyautogui
import time
import psutil


pyautogui.FAILSAFE = False
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
        pyautogui.press('down')
        #ahk.run_script('SendInput, {Down}')
        #time.sleep(1)
        #self._close_ahk()

    def arrow_up(self):
        pyautogui.press('up')
        #ahk.run_script('SendInput, {Up}')
        #time.sleep(1)
        #self._close_ahk()

    def esc(self):
        pyautogui.press('esc')
        #ahk.key_press('esc')
        #time.sleep(1)
        #self._close_ahk()

    def enter(self):
        pyautogui.press('enter')
        #ahk.key_press('enter')
        #time.sleep(1)
        #self._close_ahk()

    def tab(self):
        pyautogui.press('tab')
        time.sleep(2)

    def copy(self):
        for _ in range(2):
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)

    def copy_fast(self):
        for _ in range(2):
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
        time.sleep(1)
#
    def ctrl_i(self):
        for _ in range(2):
            pyautogui.hotkey('ctrl', 'i')
            time.sleep(1)

    def end(self):
        pyautogui.press('end')

    def _close_ahk(self):
        for proc in psutil.process_iter():
            if proc.name() == 'AutoHotkey.exe':
                proc.kill()
