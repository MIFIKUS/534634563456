import os

def get_file_sizes_in_folder(folder_path):
    file_sizes = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_sizes[file_name] = os.path.getsize(file_path)
    return file_sizes

folder_path = 'E:\Projects\PokerStarsParser\deals_files'
files_and_sizes = get_file_sizes_in_folder(folder_path)
for file, size in files_and_sizes.items():
    print(f'Файл: {file}, Размер: {size} байт')