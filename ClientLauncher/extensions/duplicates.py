import re


def delete_duplicates(path_to_file: str):
    with open(path_to_file, encoding='utf-8') as file:
        text = file.read()

    dict_of_deals = {}

    for j in text.split('\n\n'):
        text_list = j.split('\n')

        try:
            text_list.remove('')
        except Exception:
            pass

        if text_list == ['']:
            break

        necessary_rows = text_list[0:2]

        main_row = necessary_rows[0]
        hand_num = re.search(r'#(.*?):', main_row).group(1)

        dict_of_deals.update({hand_num: j})

    ready_text = '\n\n'.join(list(dict_of_deals.values()))
    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write(ready_text)

    print(f'Дубликаты из файла {path_to_file} удалены!')
