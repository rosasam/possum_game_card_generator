from __future__ import print_function
import pickle
import glob
import io
import os.path
import pandas as pd
import tqdm

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import config


def login():
    """
    Logs the user in and returns the created credentials.
    If a cached credentials exists, use that instead
    """
    creds = None

    # Define some paths relative to file location
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_path = os.path.join(dir_path, 'token.pickle')
    credentials_path = os.path.join(dir_path, config.CREDENTIALS_PATH)

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, config.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Finds all JPEG images in google drive (directory specified in config file)
def get_drive_image_list():
    creds = login()
    service = build('drive', 'v3', credentials=creds)

    images = []
    # Call the Drive v3 API
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{config.DRIVE_SOURCE_IMAGE_DIR_ID}' in parents and mimeType='image/jpeg'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            images.append({
                'name': file.get('name'),
                'id': file.get('id')
                })
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return images

def get_drive_image(img):
    file_id = img['id']
    creds = login()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    raw_img = fh.getvalue()

    source_image_dir = config.PICTURE_SOURCE_DIR
    with open(os.path.join(source_image_dir, img['name']), 'wb') as image_file:
        image_file.write(raw_img)
    fh.close()


def download_drive_images(data):
    source_image_dir = config.PICTURE_SOURCE_DIR

    # Only download images that are not already downloaded (based on image urls in spreadsheet)
    downloaded_images = glob.glob(os.path.join(source_image_dir, '*.jpg'))
    downloaded_images = [os.path.basename(d) for d in downloaded_images]
    # Images added to the spreadhsheet
    spreadsheet_images = [img for img in data["Picture"] if img]
    drive_images = get_drive_image_list()
    missing_images = [img for img in drive_images if img['name'] not in downloaded_images]
    if missing_images:
        print(f'Downloading {len(missing_images)} images from Drive...')
    for img in tqdm.tqdm(missing_images):
        get_drive_image(img)


def get_sheets_data():
    creds = login()
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME).execute()

    data = result.get('values', [])
    if not data:
        raise RuntimeError('No data found.')
    else:
        # Values is an array where each row corresponds to a row in the sheets
        return pd.DataFrame(data[1:], columns=data[0])


if __name__ == '__main__':
    print(get_all())
