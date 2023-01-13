from __future__ import print_function

import os.path
from pathlib import Path

from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from phdi.tabulation import load_schema

import csv

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.']
CREDENTIALS_FILE = 'saner-cat-23-25038f1782b1.json'
SCHEMA_FILE = 'MeasureReportSchema.yaml'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1PXovisgLzbefPVe5Til7S7kbEtdMgY6LyolZLnr98Y8'
RANGE = ''

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = service_account.Credentials.from_service_account_file('saner-cat-23-25038f1782b1.json')

    # REMOVED IN FAVOR OF SERVICE ACCOUNT
    # creds = None
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        schema = load_schema(Path('MeasureReportSchema.yaml'))
        tables = schema['tables'].keys()
        for table_name in tables:
            filename = table_name+".csv"
            if os.path.exists(filename):
                with open(filename, 'r') as datafile:
                    # Call the Sheets API
                    sheet = service.spreadsheets()

                    # The A1 notation of the values to clear.
                    data_range = table_name + RANGE

                    clear_values_request_body = {
                        # TODO: Add desired entries to the request body.
                    }

                    request = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=data_range, body=clear_values_request_body)
                    response = request.execute()
                    print(response)
                    #TODO Process clear response

                    # Get the values from the csv file
                    data = list(csv.reader(datafile))

                    # How the input data should be interpreted.
                    value_input_option = 'USER_ENTERED'

                    value_range_body = {
                        'range': data_range,
                        'values': data,
                    }

                    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=data_range, valueInputOption=value_input_option, body=value_range_body)
                    response = request.execute()
                    print(response)
                    #TODO Process update response

                    #Sample code:
                    # result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                    #                             range=table_name).execute()
                    # values = result.get('values', [])

                    # if not values:
                    #     print('No data found.')
                    #     return

                    # print('Name, Major:')
                    # for row in values:
                    #     # Print columns A and E, which correspond to indices 0 and 4.
                    #     print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()