from ClientLauncher.Google.Sheets.get_config import GetConfig
from ClientLauncher.extensions.get_config_data import get_script_name, get_pokerstars_version

import re
import json


while True:
    try:
        get_config = GetConfig()
        break
    except Exception as e:
        print(e)
        pass

SCRIPT_NAME = get_script_name()

name_details = get_config.get_name_details()

separator = name_details['separator']
free_text = name_details['free_text']


def get_info(file_path: str) -> dict or bool:
    def _get_gtd(path: str, tournament_id: str) -> str:
        with open('tournaments_data.json', 'r', encoding='utf-8') as tables_json:
            tables_info = json.load(tables_json)
            tournament_info = tables_info.get(tournament_id)
            if tournament_info:
                _gtd = tournament_info.get('gtd')
            else:
                return '0'
            if _gtd:
                return _gtd
            return '0'

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
        if get_pokerstars_version().upper() == 'ES':
            buy_in = '€' + re.search(r',\s€(.*?)\sEUR', file_list[0]).group(1)
        else:
            buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        print(buy_in)

        total_buy_in = re.search(f'BI(.*?){separator}', file_path).group(1)

        print(total_buy_in)

        if get_pokerstars_version().upper() == 'ES':
            tournament_type = re.search(f'BI{total_buy_in}{separator}(.*?){separator}', file_path).group(1)
        else:
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
            tournament_info = tables_info.get(tournament_id)
            if tournament_info:
                _gtd = tournament_info.get('gtd')
            else:
                return '0'

            if _gtd:
                return _gtd
            return '0'

    def _get_tournament_type(tournament_id: str) -> str:
        with open('tournaments_data.json', 'r', encoding='utf-8') as tables_json:
            tables_info = json.load(tables_json)
            tournament_data = tables_info.get(tournament_id)
            if tournament_data:
                return tournament_data.get('game_type')
            else:
                return '-'

    with open(f'deals_files\\{file_path}', 'r', encoding='utf-8') as file_txt:
        file_txt = file_txt.read()
        file_list = file_txt.split('\n')

        tournament_id = re.search(f'{free_text}{separator}(.*?){separator}', file_path).group(1)
        tournament_id = tournament_id.replace(' ', '').replace(free_text, '')

        print('get_info_for_tables')
        print(tournament_id)

        table_num = re.search(f'T(.*?){separator}', file_path).group(1)
        print(table_num)

        name = re.search(f'T{table_num}{separator}(.*?){separator}', file_path).group(1)
        name = name.replace(' ', '').replace(separator, '')

        print(name)

        gtd = _get_gtd(file_path, tournament_id)

        print(gtd)

        if get_pokerstars_version().upper() == 'ES':
            buy_in = '€' + re.search(r',\s€(.*?)\sEUR', file_list[0]).group(1)
        else:
            buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        print(buy_in)

        total_buy_in = re.search(f'BI(.*?){separator}', file_path).group(1)

        print(total_buy_in)

        tournament_type = _get_tournament_type(tournament_id)

        print(tournament_type)

        speed = re.search(f'MAX{separator}(.*?){separator}', file_path).group(1)
        print(speed)

        table_size = re.search(f'{separator}{tournament_type}{separator}(.*?)MAX', file_path)
        if table_size:
            table_size = table_size.group(1)
        else:
            table_size = '-'

        print(table_size)

        file_name = file_path

        print(file_name)

        hands = len(file_txt.split('PokerStars')) - 1

        print(hands)

    return {'tournament_id': tournament_id, 'table_num': table_num, 'name': name, 'gtd': gtd, 'buy_in': buy_in,
            'total_buy_in': total_buy_in, 'table_size': table_size, 'speed': speed, 'type': tournament_type,
            'file_name': file_name, 'script_name': SCRIPT_NAME, 'hands': hands}
