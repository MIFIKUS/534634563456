from ClientLauncher.Google.Sheets.url import GOOGLE_SHEET_URL
import gspread
import json


class GetConfig:
    def __init__(self):
        path_to_credentials = 'services_files\\google_credentials.json'
        self.gs = gspread.service_account(path_to_credentials)
        self.sh = self.gs.open_by_url(GOOGLE_SHEET_URL).sheet1

    def get_name_format(self) -> dict:
        while True:
            try:
                config_cells = self._open_config_cells()
                name_format_cells = config_cells.get('name_format')

                config = {}
                for cnf, cell in name_format_cells.items():
                    config.update({cnf: int(self.sh.get(cell)[0][0])})

                config = dict(sorted(config.items(), key=lambda item: item[1]))

                return config
            except Exception as e:
                print(f"ошибка в get_name_format {e}")
    def get_database_data(self) -> dict:
        while True:
            try:

                config_cells = self._open_config_cells()
                database_cells = config_cells.get('database')

                config = {}
                for cnf, cell in database_cells.items():
                    config.update({cnf: self.sh.get(cell)[0][0]})

                return config
            except Exception as e:
                print(f"ошибка в get_database_data {e}")

    def get_collect_data(self) -> dict:
        while True:
            try:
                config_cells = self._open_config_cells()
                collect_data_cells = config_cells.get('collect_data')

                config = {}
                for cnf, cell in collect_data_cells.items():
                    config.update({cnf: int(self.sh.get(cell)[0][0])})

                return config
            except Exception as e:
                print(f"ошибка в get_collect_data {e}")

    def get_name_details(self) -> dict:
        while True:
            try:
                config_cells = self._open_config_cells()
                naming_details_cells = config_cells.get('naming_details')

                config = {}
                for cnf, cell in naming_details_cells.items():
                    config.update({cnf: self.sh.get(cell)[0][0]})


                return config
            except Exception as e:
                print(f"ошибка в get_name_details {e}")

    def _open_config_cells(self) -> dict:
        path_to_config_cells = 'ClientLauncher\\Config\\config_cells.json'
        with open(path_to_config_cells) as cnf_json:
            return json.load(cnf_json)
        