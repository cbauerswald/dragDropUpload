'''
Google API
'''
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pickle
import os
import pandas as pd

'''
For Google Sheets API:
'''
def pickle_save(path, obj):
    if '.pickle' not in path:
        path += '.pickle'
    with open(path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
def pickle_load(path):
    if '.pickle' not in path:
        path += '.pickle'
    with open(path, 'rb') as handle:
        b = pickle.load(handle)
        return b

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SHEET_ID = '1EzCru8XKVSyuq0y8T-ANCYk6dy_hZq5nBPs4ATaIOXI'


def sheets_auth(token_path = '../creds/token.pickle', creds_path = '../creds/credentials.json'):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
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
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def get_sheet(service, sheet_name, id_ = SHEET_ID):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id_, range=f'{sheet_name}!A:G').execute()
    values = result.get('values', [])
    df = pd.DataFrame.from_records(values).fillna('N/A')
    h = df.iloc[0]
    df = df.iloc[1:]
    df.columns = h
    return df