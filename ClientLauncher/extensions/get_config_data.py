import json


def open_file():
    with open('config.json', 'r', encoding='utf-8') as config_json:
        return json.load(config_json)


def get_script_name() -> str:
    config = open_file()
    return config['SCRIPT_NAME']


def get_google_row() -> int:
    config = open_file()
    return config['GOOGLE_SHEETS_ROW']