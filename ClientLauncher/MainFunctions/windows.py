from ctypes import windll
from ClientLauncher.extensions.error_handler import endless_error_handler

import win32gui
import win32com.client
import win32con

import re

user32 = windll.user32
user32.SetProcessDPIAware()


class Windows:
    def __init__(self):
        self.TOURNAMENT_WINDOW_SIZE = (969, 696)
        self._main_window_name = 'PokerStars Lobby'
        self._tournament_window_name = 'Table'

    @endless_error_handler
    def get_main_window(self):
        shell = win32com.client.Dispatch("WScript.Shell")

        window = self._find_windows(self._main_window_name)[0]

        shell.SendKeys('%')
        win32gui.ShowWindow(window, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window)
        self.open_fullscreen_window_by_hwnd(window)
        return window

    @endless_error_handler
    def get_tournament_window(self):
        shell = win32com.client.Dispatch("WScript.Shell")

        window = self._find_windows(self._tournament_window_name)

        shell.SendKeys('%')
        win32gui.ShowWindow(window, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window)
        return window

    @endless_error_handler
    def open_window_by_hwnd(self, hwnd):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

    @endless_error_handler
    def open_fullscreen_window_by_hwnd(self, hwnd):
        def _is_fullscreen(hwnd):
            full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
            try:
                rect = win32gui.GetWindowRect(hwnd)
                return rect == full_screen_rect
            except:
                return False

        if not _is_fullscreen(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    @endless_error_handler
    def open_small_window_by_hwnd(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    @endless_error_handler
    def _find_windows(self, window_name):
        def __is_toplevel(hwnd):
            try:
                return win32gui.GetParent(hwnd) == 0 and win32gui.IsWindowVisible(hwnd)
            except Exception:
                return None

        hwnd_list = []

        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd) if __is_toplevel(hwnd) else None, hwnd_list)

        lst_processes = [hwnd for hwnd in hwnd_list if window_name in win32gui.GetWindowText(hwnd)]

        if lst_processes:
            return lst_processes
        else:
            return None

    @endless_error_handler
    def close_window_by_hwnd(self, hwnd):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    @endless_error_handler
    def get_window_size_by_hwnd(self, hwnd) -> tuple:
        size = win32gui.GetWindowRect(hwnd)
        x = size[0]
        y = size[1]
        w = size[2] - x
        h = size[3] - y
        return w, h

    @endless_error_handler
    def open_instant_hand_history_menu(self):
        hwnd = self._find_windows('Instant Hand History')[0]
        self.open_window_by_hwnd(hwnd)

    @endless_error_handler
    def find_all_tables_windows(self):
        tables_list = []

        tables = self._find_windows('Table')
        if tables:
            for i in tables:
                table_text = win32gui.GetWindowText(i)

                table_id = re.search(r'Tournament\s(.*?)\sTable', table_text).group(1)
                table_num = re.search(r'Table(.*)$', table_text).group(1)

                table_text_final = table_id + ' ' + table_num

                tables_list.append(table_text_final)
            return tables_list
        return []

    @endless_error_handler
    def get_hwnd_by_name(self, name):
        return self._find_windows(name)[0]

    @endless_error_handler
    def get_amount_of_opened_tables(self):
        return len(self.find_all_tables_windows())