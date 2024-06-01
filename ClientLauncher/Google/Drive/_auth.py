from google.oauth2 import service_account
from googleapiclient.discovery import build


class ServiceAcc:
    def __init__(self, service_acc_file='services_files\\google_credentials.json'):
        self._service_acc_file = service_acc_file
        self._scopes = ['https://www.googleapis.com/auth/drive']

        self._credentials = service_account.Credentials.from_service_account_file(
            self._service_acc_file, scopes=self._scopes)
        self.service = build('drive', 'v3', credentials=self._credentials)

    def get_service(self):
        return self.service
