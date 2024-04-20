from googleapiclient.http import MediaIoBaseDownload
from ClientLauncher.Google.Drive._auth import ServiceAcc
import io

auth = ServiceAcc()


class DownloadDeals:
    def __init__(self):
        self._service = auth.get_service()

    def get_all_files(self):
        results = self._service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()

        return results

    def download_file(self, file_id, filename, path_to_save):
        request = self._service.files().get_media(fileId=file_id)
        fh = io.FileIO(f'{path_to_save}\\{filename}', 'wb')

        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        print('Файл скачан')
