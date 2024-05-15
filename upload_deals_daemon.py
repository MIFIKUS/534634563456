from ClientLauncher.Google.Drive.upload import UploadDeals
from ClientLauncher.Database import get_info_from_file
from ClientLauncher.Database.add_info import AddInfo

import os

PATH_TO_DEALS = 'deals_files'

upload = UploadDeals()
add_db_info = AddInfo()


def get_filled_files(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            if os.path.getsize(file_path) > 0:
                files.append(file_name)

    return files


while True:
    files = get_filled_files(PATH_TO_DEALS)
    if files:
        for i in files:
            print(f'Попытка получить информацию для БД из файла {i}')
            file_data = get_info_from_file.get_info(f'{i}')
            if not file_data
                print('Не удалось получить информацию для БД')
            else:
                file_data_for_tables = get_info_from_file.get_info_for_tables(i)
                print('Удалось получить информацию')

                add_db_info.add_main_archive_info(file_data)
                add_db_info.add_tables_main_info(file_data_for_tables)

            print(f'Попытка загрузить на гугл диск файл {i}')
            try:
                upload.upload_deal(i)
                print('Удалось загрузить файл')
                print('Попытка удалить файл')
                try:
                    os.remove(f'deals_files\\{i}')
                    print('Удалось удалить файл')
                except Exception as e:
                    print(f'Не удалось удалить файл Ошибка {e}')
            except Exception as e:
                print(f'Не удалось загрузить файл Ошибка {e}')
