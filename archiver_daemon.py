from ClientLauncher.Google.Drive.download import DownloadDeals
from ClientLauncher.Google.Drive.delete import DeleteDeal
from ClientLauncher.Google.Sheets.get_config import GetConfig

import zipfile
import os
import re


download = DownloadDeals()
delete = DeleteDeal()
config = GetConfig()

DELAY = 20
PATH_TO_SAVE = 'E:\\poker'

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

def check_if_archive_exists(file_name: str):
    file_name = file_name.replace('.txt', '.rar')

    if file_name in os.listdir(PATH_TO_SAVE):
        return True
    return False

def get_filename(filename):
    pattern = f'T(.*?){separator}'
    result = re.search(pattern, filename)
    if result:
        table_num = result.group(1)
        filename_without_table_num = filename.replace(f'T{table_num}{separator}', '')
        return filename_without_table_num + '.zip'
    else:
        return False


while True:
    files = download.get_all_files()
    data = get_filenames_and_ids(files)
    print(data)
    if data:
        for file_name, file_id in data.items():
            file_name = get_filename(file_name)
            download.download_file(file_id, file_name, PATH_TO_SAVE)
            if check_if_archive_exists(file_name):
                with zipfile.ZipFile(f'{PATH_TO_SAVE}\\{file_name.replace('.txt', '.zip')}', 'a') as zipf:
                    zipf.write(f'{PATH_TO_SAVE}\\{file_name}')
            else:
                with zipfile.ZipFile(f'{PATH_TO_SAVE}\\{file_name.replace('.txt', '.zip')}', 'w') as zipf:
                    zipf.write(f'{PATH_TO_SAVE}\\{file_name}')
            os.remove(f'{PATH_TO_SAVE}\\{file_name}')
            delete.delete_deal(file_id)
