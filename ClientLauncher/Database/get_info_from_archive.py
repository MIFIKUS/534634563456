from ClientLauncher.Google.Sheets.get_config import GetConfig
import re
import zipfile


while True:
    try:
        get_config = GetConfig()
        break
    except Exception:
        pass


name_details = get_config.get_name_details()
separator = name_details['separator']
free_text = name_details['free_text']


def get_info(file_path: str) -> dict:
    with zipfile.ZipFile(file_path, 'r') as zipf:
        tournament_id = re.search(f'{free_text}{separator}(.*?){separator}', file_path.split('\\')[-1]).group(1)
        files_in_archive = len(zipf.namelist())
        hands = 0

        for i in zipf.namelist():
            content = zipf.read(i).decode('utf-8')
            print(len(content.split('\n\n')))
            hands += len(re.split(r'\n\s*\n', content))

        return {'tournament_id': tournament_id, 'files_in_archive': files_in_archive, 'hands': hands}
