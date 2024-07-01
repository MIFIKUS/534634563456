import traceback

from ClientLauncher.Google.Drive.upload import UploadDeals
from ClientLauncher.Database import get_info_from_file
from ClientLauncher.Database.add_info import AddInfo

from datetime import datetime

import os
import logging

logging.basicConfig(level=logging.DEBUG, filename=f'logs\\upload_deals_{datetime.now().strftime("%d_%m_%Y")}.log',
                    filemode='a', encoding='utf-8', format="%(asctime)s %(levelname)s %(message)s")

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
        logging.debug('Есть файлы которые можно добавить в диск')
        print('Есть файлы которые можно добавить в диск')
        for i in files:
            try:
                logging.debug(f'Попытка получить информацию для БД из файла {i}')
                print(f'Попытка получить информацию для БД из файла {i}')

                file_data = get_info_from_file.get_info(f'{i}')

                if not file_data:
                    print('Не удалось получить информацию для бд')
                    logging.warning('Не удалось получить информацию для БД')
                else:
                    print('file_data получена')
                    file_data_for_tables = get_info_from_file.get_info_for_tables(i)
                    print("Попытка отправить в бд")
                    add_db_info.add_main_archive_info(file_data)
                    print("В бд отправлено")

                    print("Попытка отправить в бд")
                    add_db_info.add_tables_main_info(file_data_for_tables)
                    print("В бд отправлено")

                try:
                    print('попытка отправить файл на гугл диск')
                    upload.upload_deal(i)
                    try:
                        os.remove(f'deals_files\\{i}')
                    except Exception as e:
                        print(f'Не удалось удалить файл Ошибка {e}')
                except Exception as e:
                    print(f'Не удалось загрузить файл Ошибка {e}')
                    continue
            except Exception as e:
                traceback.print_exc()
                continue
