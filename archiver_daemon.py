from ClientLauncher.Google.Drive.download import DownloadDeals
from ClientLauncher.Google.Drive.delete import DeleteDeal
from ClientLauncher.Google.Sheets.get_config import GetConfig

from ClientLauncher.Database.add_info import AddInfo
from ClientLauncher.Database.get_info_from_archive import get_info

from ClientLauncher.extensions.error_handler import do_without_error

import zipfile
import os
import re
import time


add_info_to_db = AddInfo()

while True:
    try:
        config = GetConfig()
        break
    except Exception as e:
        print(f'Ошибка при инициализации GetConfig {e}')


DELAY = 20
PATH_TO_SAVE = 'D:\\deals'

name_details = config.get_name_details()

separator = name_details['separator']
free_text = name_details['free_text']


def get_filenames_and_ids(files):
    if files:
        filenames_and_ids = {}

        files_list = files['files']
        for file in files_list:
            if '.txt' in file['name']:
                filenames_and_ids.update({file['name']: file['id']})

        return filenames_and_ids


def get_tournament_id(filename: str) -> str:
    return re.search(r'PS__(.*?)__T', filename).group(1)


def check_if_archive_exists(tournament_id: str) -> bool:
    for i in os.listdir(PATH_TO_SAVE):
        existed_tournament_id = get_tournament_id(i)
        if tournament_id == existed_tournament_id:
            return True
    return False


def get_filename(filename):
    pattern = f'T(.*?){separator}'
    result = re.search(pattern, filename)
    if result:
        table_num = result.group(1)
        filename_without_table_num = filename.replace(f'T{table_num}{separator}', '')
        return filename_without_table_num.replace('.txt', '.zip')
    else:
        return False


while True:
    for acc_file in os.listdir('services_files'):
        acc_file_path = f'services_files\\{acc_file}'

        download = DownloadDeals(acc_file_path)
        delete = DeleteDeal(acc_file_path)

        files = download.get_all_files()
        data = get_filenames_and_ids(files)
        print(data)
        if data:
            for file_name, file_id in data.items():

                file_name_for_archive = get_filename(file_name)
                tournament_id = get_tournament_id(file_name)

                download.download_file(file_id, file_name, PATH_TO_SAVE)
                print(f'file_name {file_name} archive_name {file_name_for_archive}')

                if check_if_archive_exists(tournament_id):
                    print('Archive exists')
                    with zipfile.ZipFile(f'{PATH_TO_SAVE}\\{file_name_for_archive}', 'a') as zipf:
                        if file_name not in zipf.namelist():
                            zipf.write(f'{PATH_TO_SAVE}\\{file_name}', arcname=f'{PATH_TO_SAVE}\\{file_name}'.split('\\')[-1])
                else:
                    with zipfile.ZipFile(f'{PATH_TO_SAVE}\\{file_name_for_archive}', 'w') as zipf:
                        print('Archive created')
                        if file_name not in zipf.namelist():
                            zipf.write(f'{PATH_TO_SAVE}\\{file_name}', arcname=f'{PATH_TO_SAVE}\\{file_name}'.split('\\')[-1])

                print(f'Попытка получить информацию для бд из архива {file_name_for_archive}')
                archive_data_for_db = get_info(f'{PATH_TO_SAVE}\\{file_name_for_archive}')

                do_without_error(add_info_to_db.add_additional_archive_info, archive_data_for_db)

                os.remove(f'{PATH_TO_SAVE}\\{file_name}')
                delete.delete_deal(file_id)
                time.sleep(2)
