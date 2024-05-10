import win32gui
import re
import time

time.sleep(2)
hwnd = win32gui.GetForegroundWindow()
header = win32gui.GetWindowText(hwnd)
a =  re.search(r', (\$.+?) Gtd', header).group(1)

print(a)