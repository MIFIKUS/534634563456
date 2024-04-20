from googleapiclient.http import MediaIoBaseDownload
from ClientLauncher.Google.Drive._auth import ServiceAcc


auth = ServiceAcc()


class DownloadDeals:
    def __init__(self):
        self._service = auth.get_service()

    def get_all_files(self):
        results = self._service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()

        print(results)

    