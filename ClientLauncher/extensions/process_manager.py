import win32gui
import win32con


def kill_lobby_windows():
    def enum_handler(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if 'Lobby' in title and 'Tournament' in title:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    win32gui.EnumWindows(enum_handler, None)
