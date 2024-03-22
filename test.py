import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

service_account_info = json.load(open('services_files\\google_credentials.json'))
creds=Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=creds)

def uploadFile():
    file_metadata = {
    'name': 'closed_tables.txt',
    'mimeType': '*/*',
    'parents': '1UlZpjkzLSb-gKo0rjv1BCNRcwfk1sHl_'
    }
    media = MediaFileUpload('closed_tables.txt',
                            mimetype='*/*',
                            resumable=True,)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: ' + file.get('id'))

uploadFile()