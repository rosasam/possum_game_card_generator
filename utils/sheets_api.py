from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# 'All cards' spreadsheet ID
SPREADSHEET_ID = '1yJsNpidAPBM8KogZp611Ebn-r0iaY9_1g5bkOW0XOM0'

TAB = 'All cards'
RANGE = 'A2:F'
RANGE_NAME = f"'{TAB}'!{RANGE}"


def login():
    """
    Logs the user in and returns the created credentials.
    If a cached credentials exists, use that instead
    """
    creds = None

    # Define some paths relative to file location
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_path = os.path.join(dir_path, 'token.pickle')
    credentials_path = os.path.join(dir_path, 'credentials.json')

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
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_all():
    creds = login()
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        raise RuntimeError('No data found.')
    else:
        # Values is an array where each row corresponds to a row in the sheets
        return values


if __name__ == '__main__':
    print(get_all())