import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'EuropeanColl_Creds.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1k_R751jO2aYwUIcH2slnwspxT0FnlN9amuTRLj9mE6A'
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='JSON_Raw_Py!A1:Z20').execute()
values = result.get('values', [])

print(values)

