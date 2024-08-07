from ClientLauncher.Google.Sheets.get_config import GetConfig
from ClientLauncher.extensions.get_config_data import get_pokerstars_version

import datetime
import string

import pytz


while True:
    try:
        config = GetConfig()
        break
    except Exception as e:
        print(f'Ошибка при инициализации GetConfig {e}')


class CreateFileName:
    def __init__(self):
        self._name_format = config.get_name_format()
        self._name_details = config.get_name_details()
        self._separator = self._name_details['separator']
        self._free_text = self._name_details['free_text']

    def get_file_name(self, data: dict, table_num) -> str:
        table_num = str(table_num)
        print(data)
        file_name = ''
        counter = 0
        for row, value in self._name_format.items():
            print(row)
            counter += 1
            if value == 0:
                print(f'Для {row} установлено значение 0')
                continue

            if row == 'free_text':
                file_name += self._name_details['free_text']
            elif row == 'table_num':
                file_name += 'T' + table_num
            elif row == 'creation_date':
                file_name += str(datetime.datetime.now(pytz.timezone('Etc/GMT+1')).strftime("%Y_%m_%d"))
            elif row == 'buy_in':
                file_name += 'BI' + data.get(row)
            elif row == 'players_amount':
                file_name += str(data.get(row)) + 'MAX'
            elif row == 'tournament_name':
                tournament_name = str(data.get(row))
                tournament_name = tournament_name.replace(' ', '_')
                tournament_name = tournament_name.replace(':', '')

                file_name += tournament_name
            else:

                if data.get(row) is None:
                    text = 'ERROR'
                else:
                    text = data.get(row)
                file_name += text
                print(file_name)
            if counter != len(self._name_format):
                file_name += self._separator

        return file_name + '.txt'


