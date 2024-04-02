from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.mouse_and_keyboard import Keyboard
from ClientLauncher.extensions import game_types

from tkinter import Tk

image = Image()
keyboard = Keyboard()

class GetType:
    def __init__(self):
        self._list_of_speeds = [
            'turbo.png',
            'hyper_turbo.png',
            'slow.png',
            'regular.png'
        ]
        self._list_of_game_types = [
            'progressive.png',
            'total_progressive.png'
        ]
        self._list_of_players_amount = {
            6: {'low':  [60, 150, 50],
                'high': [100, 200, 110]},
            7: {'low':  [0, 130, 100],
                'high': [20, 200, 150]},
            2: {'low':  [200, 0, 10],
                'high': [240, 10, 50]},
            8: {'low':  [70, 190, 210],
                'high': [130, 230, 255]},
            9: {'low':  [90, 90, 90],
                'high': [110, 110, 110]}
        }

    def get_header_info(self, num):
        tournament_id = self._get_tournament_id()
        game_type = self._get_tourney_game_type(num)
        speed = self._get_tourney_speed(num)
        players_amount = self._get_tourney_players_amount(num)
        buy_in = self._get_tourney_buy_in(num)

        return {tournament_id: {'game_type': game_type, 'speed': speed, 'players_amount': players_amount, 'buy_in': buy_in}}

    def _get_tournament_id(self):
        keyboard.copy()
        return Tk().clipboard_get()

    def _get_tourney_speed(self, num):
        SPEED_LIST = {
            'regular.png': 'REG',
            'turbo.png': 'TURBO',
            'hyper_turbo.png': 'HYPER',
            'slow.png': 'SLOW'
        }

        image.take_screenshot('imgs\\screenshots\\speed\\tourney_speed.png', area_of_screenshot=(484, 251 + (num * 26),
                                                                                                             501, 262 + (num * 26)))
        path_to_speed_templates = 'imgs\\templates\\speed\\'

        for i in self._list_of_speeds:
            if image.matching('imgs\\screenshots\\speed\\tourney_speed.png', path_to_speed_templates+i):
                return SPEED_LIST.get(i)

    def _get_tourney_game_type(self, num):
        image.take_screenshot('imgs\\screenshots\\knockouts\\game_type.png', area_of_screenshot=(467, 250 + (num * 26),
                                                                                                             482, 263 + (num * 26)))

        path_to_knockouts_templates = 'imgs\\templates\\knockouts\\'

        is_there_knockout = False
        for i in self._list_of_game_types:
            if image.matching('imgs\\screenshots\\knockouts\\game_type.png', path_to_knockouts_templates+i):
                is_there_knockout = True

        if is_there_knockout:
            image.take_screenshot('imgs\\screenshots\\knockouts\\game_type_color.png', area_of_screenshot=(470, 256 + (num * 26),
                                                                                                                       471, 257 + (num * 26)))

            if image.matching('imgs\\screenshots\\knockouts\\game_type_color.png', 'imgs\\templates\\knockouts\\progressive.png'):
                return 'KO'
            else:
                return 'FREEZE'

            #color = image.get_main_color('imgs\\screenshots\\knockouts\\game_type_color.png')

            #if 200 <= color[0] <= 250 and 40 <= color[1] <= 80 and 60 <= color[2] <= 110:
            #    return 'KO'
            #elif 220 <= color[0] <= 255 and 200 <= color[1] <= 255 and 130 <= color[2] <= 200:
            #    return 'KO'
            #else:
            #    return 'FREEZE'

    def _get_tourney_players_amount(self, num):
        image.take_screenshot('imgs\\screenshots\\players_amount\\players_amount_color.png', area_of_screenshot=(506, 250 + (num * 26),
                                                  507, 263 + (num * 26)))
        color = image.get_main_color('imgs\\screenshots\\players_amount\\players_amount_color.png')

        for amount, color_list in self._list_of_players_amount.items():
            color_min = color_list.get('low')
            color_max = color_list.get('high')
            if color_min[0] <= color[0] <= color_max[0] and color_min[1] <= color[1] <= color_max[1] and color_min[2] <= color[2] <= color_max[2]:
                return amount
        return False

    def _get_tourney_buy_in(self, num):
        image.take_screenshot('imgs\\screenshots\\buy_in\\buy_in.png',
                              area_of_screenshot=(580, 250 + (num * 26),
                                                  680, 263 + (num * 26)))
        buy_in = image.image_to_string('imgs\\screenshots\\buy_in\\buy_in.png', True)

        buy_in = buy_in.replace('\n', '')
        buy_in = buy_in.replace(',', '')

        if buy_in[-1] == '.':
            buy_in = buy_in[0:-1]

        return buy_in
