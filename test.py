from google.oauth2 import service_account
from googleapiclient.discovery import build




_scopes = ['https://www.googleapis.com/auth/drive']

_credentials = service_account.Credentials.from_service_account_file('google_credentials.json', scopes=_scopes)
_service = build('drive', 'v3', credentials=_credentials)



results = _service.files().list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()

print(results)
