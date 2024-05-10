from ClientLauncher.Google.Sheets.get_config import GetConfig
import re


while True:
    try:
        get_config = GetConfig()
        break
    except Exception:
        pass


def get_info(file_path: str) -> dict:
    name_details = get_config.get_name_details()

    separator = name_details['separator']
    free_text = name_details['free_text']

    with open(f'deals_files\\{file_path}', 'r', encoding='utf-8') as file_txt:
        file_list = file_txt.read().split('\n')

        id = re.search(f'{free_text}{separator}(.*?){separator}', file_path).group(1)
        id = int(id.replace(' ', '').replace(free_text, ''))

        print(id)

        table_num = re.search(f'T(.*?){separator}', file_path).group(1)
        table_num = 'T' + table_num.replace(' ','').replace(separator, '')

        print(table_num)

        name = re.search(f'{table_num}{separator}(.*?){separator}', file_path).group(1)
        name = name.replace(' ', '').replace(separator, '')

        print(name)

        #сюда gtd
        gtd = ''

        buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        print(buy_in)

        total_buy_in = re.search(f'BI(.*?){separator}', file_path).group(1)

        print(f'BI{total_buy_in}{separator} {separator}')

        tournament_type = re.search(f'{total_buy_in.replace('$', '')}{separator}(.*?){separator}', file_path).group(1)

        table_size = re.search(f'{separator}{tournament_type}{separator}(.*?)MAX', file_path).group(1)
        print(table_size)

        speed = re.search(f'MAX{separator}(.*?){separator}', file_path).group(1)

        archive_name = file_path.replace(f'{table_num}{separator}', '').replace('.txt', '.zip')

    return {'tournament_id': id, 'name': name, 'gtd': gtd, 'buy_in': buy_in, 'total_buy_in': total_buy_in,
            'table_size': table_size, 'speed': speed, 'type': tournament_type, 'archive_name': archive_name}



    return dict()

