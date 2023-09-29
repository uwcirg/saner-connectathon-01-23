from __future__ import print_function

import os.path
from pathlib import Path
from datetime import datetime

from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from phdi.tabulation import load_schema

import csv
import numpy as np

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.']
CREDENTIALS_FILE = 'credentials.json'
SCHEMA_FILE = 'MeasureReportSchema.yaml'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1PXovisgLzbefPVe5Til7S7kbEtdMgY6LyolZLnr98Y8'
DATA_RANGE = ''
SUMMARY_RANGE='Summary!A:D'

def getRange(sheets, range):
    request = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range)
    response = request.execute()
    values = response.get('values', [])

    if not values:
        print('No data found at '+range)
        return []

    return values

def clearRange(sheets, range):
    clear_values_request_body = {
        # TODO: Add desired entries to the request body.
    }
    request = sheets.values().clear(spreadsheetId=SPREADSHEET_ID, range=range, body=clear_values_request_body)
    response = request.execute()
    return response

def updateRange(sheets, range, values):
    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        'range': range,
        'values': values,
    }
    request = sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    return response

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)

    try:
        service = build('sheets', 'v4', credentials=creds)

        schema = load_schema(Path('MeasureReportSchema.yaml'))
        tables = schema['tables'].keys()
        for table_name in tables:
            filename = table_name+".csv"
            if os.path.exists(filename):
                with open(filename, 'r') as datafile:

                    # Call the Sheets API
                    sheets = service.spreadsheets()

                    # The A1 notation of the values to clear.
                    data_range = table_name + DATA_RANGE

                    values = list(csv.reader(datafile))
                    current_sheet_values = getRange(sheets, data_range)
                    print(len(values))
                    print(len(current_sheet_values))
                    print("Got current values")
                    # unique = list(set(values) & set(current_sheet_values))
                    new_values = [i for i in values if i not in current_sheet_values]
                    deleted_values = [i for i in current_sheet_values if i not in values]

                    if len(new_values) > 0 or len(deleted_values) > 0:
                        print()
                        # Something changed, update the sheet and log
                        summary_values = getRange(sheets=sheets, range=SUMMARY_RANGE)

                        updated_col = values[0].index('Updated')
                        max_updated_time = max(np.array(new_values)[:,updated_col])
                        
                        summary_values.append([str(datetime.now()), max_updated_time, len(new_values), len(deleted_values)])
                        # Add the summary
                        clear_response = clearRange(sheets, SUMMARY_RANGE)
                        update_response = updateRange(sheets, SUMMARY_RANGE, summary_values)
                        # Add the data
                        clear_response = clearRange(sheets, data_range)
                        update_response = updateRange(sheets, data_range, values)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()