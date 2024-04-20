from googleapiclient.http import MediaFileUpload
from ClientLauncher.Google.Drive._auth import ServiceAcc


auth = ServiceAcc()


class UploadDeals:
    def __init__(self):
        self._service = auth.get_service()

    def upload_deal(self, deal: str):
        path = f'deals_files\\{deal}'
        metadata = {
            'name': deal
        }

        media = MediaFileUpload(path, resumable=True)
        self._service.files().create(body=metadata, media_body=media, fields='id').execute()
