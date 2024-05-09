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

        table_num = re.search(f'T(.*?){separator}', file_path).group(1)
        table_num = 'T' + table_num.replace(' ','').replace(separator, '')

        name = re.search(f'{table_num}{separator}(.*?){separator}', file_path).group(1)
        name = name.replace(' ', '').replace(separator, '')

        #сюда gtd

        buy_in = '$' + re.search(r',\s\$(.*?)\sUSD', file_list[0]).group(1)

        total_buy_in = re.search(f'BI{separator}(.*?){separator}', file_path).group(1)

        table_size = re.search(f'{separator}(.*?)MAX', file_path).group(1)



    return dict()

