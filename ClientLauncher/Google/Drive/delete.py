from ClientLauncher.Google.Drive._auth import ServiceAcc
from ClientLauncher.Google.Drive.download import DownloadDeals
import time


class DeleteDeal:
    def __init__(self, acc_file):
        self.auth = ServiceAcc(acc_file)
        self.download = DownloadDeals(acc_file)
        self._service = self.auth.get_service()

    def delete_deal(self, file_id):
        while True:
            try:
                self._service.files().delete(fileId=file_id).execute()
                time.sleep(2)
                if file_id in self.download.get_all_files_id():
                    continue
            except Exception:
                return
