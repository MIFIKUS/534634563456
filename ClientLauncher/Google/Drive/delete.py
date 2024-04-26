from ClientLauncher.Google.Drive._auth import ServiceAcc
from ClientLauncher.Google.Drive.download import DownloadDeals
import time

auth = ServiceAcc()
download = DownloadDeals()


class DeleteDeal:
    def __init__(self):
        self._serice = auth.get_service()

    def delete_deal(self, file_id):
        while True:
            try:
                self._serice.files().delete(fileId=file_id).execute()
                time.sleep(2)
                if file_id in download.get_all_files_id():
                    continue
            except Exception:
                return
