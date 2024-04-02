from ClientLauncher.Statistics.get_ip import get_ip
from ClientLauncher.Google.Sheets.url import GOOGLE_SHEET_URL
import gspread
import json


class GetStatistics:
    def __init__(self):
        path_to_credentials = 'services_files\\google_credentials.json'
        self.gs = gspread.service_account(path_to_credentials)
        self.sh = self.gs.open_by_url(GOOGLE_SHEET_URL).get_worksheet(1)
        self._ip = get_ip()
        self._row = self._get_cell_num_for_client()

    def get_open_tables(self):
        statistics_file = self._open_statistics_file()
        statistics_cell = statistics_file.get('opened_tables')

        return int(self.sh.get(f'{statistics_cell}{self._row}')[0][0])

    def _open_statistics_file(self):
        with open('ClientLauncher\\Statistics\\statistics_cells.json') as statistics_json:
            return json.load(statistics_json)

    def _get_cell_num_for_client(self):
        print(self._ip)
        return self.sh.find(self._ip).row