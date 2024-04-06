from ClientLauncher.Google.Sheets.url import GOOGLE_SHEET_URL
from ClientLauncher.Statistics.get_ip import get_ip

import gspread
import json


class WriteStatistics:
    def __init__(self):
        path_to_credentials = 'services_files\\google_credentials.json'
        self.gs = gspread.service_account(path_to_credentials)
        self.sh = self.gs.open_by_url(GOOGLE_SHEET_URL).get_worksheet(1)
        self._ip = get_ip()
        self.client_row = 2

    def set_status(self, status):
        cells = self._open_cells_file()
        status_cell = cells.get('status')

        self.sh.update(f'{status_cell}{self.client_row}', [[status]])

    def set_opened_tables(self, opened_tables: int):
        cells = self._open_cells_file()
        opened_tables_cell = cells.get('opened_tables')

        self.sh.update(f'{opened_tables_cell}{self.client_row}', [[opened_tables]])

    def set_files_per_hour(self, files_per_hour: int):
        cells = self._open_cells_file()
        files_per_hour_cell = cells.get('files')

        self.sh.update(f'{files_per_hour_cell}{self.client_row}', [[files_per_hour]])

    def set_deals_per_hour(self, deals_per_hour: int):
        cells = self._open_cells_file()
        deals_per_hour_cell = cells.get('deals')

        self.sh.update(f'{deals_per_hour_cell}{self.client_row}', [[deals_per_hour]])

    def _open_cells_file(self):
        with open('ClientLauncher\\Statistics\\statistics_cells.json') as cells_json:
            return json.load(cells_json)

    def _get_cell_num_for_client(self):
        print(self._ip)
        return self.sh.find(self._ip).row
