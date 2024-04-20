from ClientLauncher.Google.Drive._auth import ServiceAcc
import time

auth = ServiceAcc()

class DeleteDeal:
    def __init__(self):
        self._serice = auth.get_service()

    def delete_deal(self, file_id):
        self._serice.files().delete(fileId=file_id).execute()
        time.sleep(2)