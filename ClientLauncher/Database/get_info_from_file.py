from ClientLauncher.Google.Sheets.get_config import GetConfig
from ClientLauncher.extensions.get_config_data import get_script_name

import re
import json


while True:
    try:
        get_config = GetConfig()
        break
    except Exception:
        pass

SCRIPT_NAME = get_script_name()

name_details = get_config.get_name_details()

separator = name_details['separator']
free_text = name_details['free_text']


def get_info(file_path: str) -> dict or bool:
    def _get_gtd(path: str, tournament_id: str) -> str:
        with open('tournaments_data.json', 'r', encoding='utf-8') as tables_json:
            tables_info = json.load(tables_json)

            return tables_info[tournament_id]['gtd']

    with open(f'deals_files\\{file_path}', 'r', encoding='utf-8') as file_txt:
        if not file_txt:
            return False
        file_list = file_txt.read().split('\n')

        id = re.search(f'{free_text}{separator}(.*?){separator}', file_path).group(1)
        id = id.replace(' ', '').replace(free_text, '')

        print(id)

        table_num = re.search(f'T(.*?){separator}', file_path).group(1)
        table_num = 'T' + table_num.replace(' ','').replace(separator, '')

        print(table_num)

        name = re.search(f'{table_num}{separator}(.*?){separator}', file_path).group(1)
        name = name.replace(' ', '').replace(separator, '')

        print(name)

        #сюда gtd
        gtd = _get_gtd(file_path, id)

        buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        print(buy_in)

        total_buy_in = re.search(f'BI(.*?){separator}', file_path).group(1)

        print(total_buy_in)

        tournament_type = re.search(f'BI{total_buy_in.replace('$', r'\$')}{separator}(.*?){separator}', file_path).group(1)
        print(tournament_type)
        table_size = re.search(f'{separator}{tournament_type}{separator}(.*?)MAX', file_path).group(1)
        print(table_size)

        speed = re.search(f'MAX{separator}(.*?){separator}', file_path).group(1)

        archive_name = file_path.replace(f'{table_num}{separator}', '').replace('.txt', '.zip')

    return {'tournament_id': id, 'name': name, 'gtd': gtd, 'buy_in': buy_in, 'total_buy_in': total_buy_in,
            'table_size': table_size, 'speed': speed, 'type': tournament_type, 'archive_name': archive_name}


def get_info_for_tables(file_path: str) -> dict:
    def _get_gtd(path: str, tournament_id: str) -> str:
        with open('tournaments_data.json', 'r', encoding='utf-8') as tables_json:
            tables_info = json.load(tables_json)

            return tables_info[tournament_id]['gtd']

    def _get_tournament_type(tournament_id: str) -> str:
        with open('tournaments_data.json', 'r', encoding='utf-8') as tables_json:
            tables_info = json.load(tables_json)

            return tables_info[tournament_id]['game_type']

    with open(f'deals_files\\{file_path}', 'r', encoding='utf-8') as file_txt:
        file_txt = file_txt.read()
        file_list = file_txt.split('\n')

        tournament_id = re.search(f'{free_text}{separator}(.*?){separator}', file_path).group(1)
        tournament_id = tournament_id.replace(' ', '').replace(free_text, '')

        print('get_info_for_tables')
        print(tournament_id)

        table_num = re.search(f'T(.*?){separator}', file_path).group(1)
        print(table_num)

        name = re.search(f'{table_num}{separator}(.*?){separator}', file_path).group(1)
        name = name.replace(' ', '').replace(separator, '')

        print(name)

        gtd = _get_gtd(file_path, tournament_id)

        print(gtd)

        buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        print(buy_in)

        total_buy_in = re.search(f'BI(.*?){separator}', file_path).group(1)

        print(total_buy_in)

        tournament_type = _get_tournament_type(tournament_id)

        print(tournament_type)

        table_size = re.search(f'{separator}{tournament_type}{separator}(.*?)MAX', file_path).group(1)

        print(table_size)

        speed = re.search(f'MAX{separator}(.*?){separator}', file_path).group(1)
        print(speed)

        file_name = file_path

        print(file_name)

        hands = len(file_txt.split('\n\n'))

        print(hands)

    return {'tournament_id': tournament_id, 'table_num': table_num, 'name': name, 'gtd': gtd, 'buy_in': buy_in,
            'total_buy_in': total_buy_in, 'table_size': table_size, 'speed': speed, 'type': tournament_type,
            'file_name': file_name, 'script_name': SCRIPT_NAME, 'hands': hands}
