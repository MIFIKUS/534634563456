import win32gui



hwnd = win32gui.GetForegroundWindow()

print(win32gui.GetWindowText(hwnd))