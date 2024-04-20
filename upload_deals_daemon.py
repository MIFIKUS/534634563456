import os
from ClientLauncher.Google.Drive.upload import UploadDeals
import os

PATH_TO_DEALS = 'deals_files'

upload = UploadDeals()


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
