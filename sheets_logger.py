import json
import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "1OWRp1CgJd-oNoukHyayU8tASqS40ibNdjNnnT0tCB2w" # Your Sheet ID

def get_service():
    creds_json = os.getenv("SERVICE_ACCOUNT_JSON")
    
    if creds_json:
        info = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        # Local filename must match your uploaded file
        credentials = service_account.Credentials.from_service_account_file(
            'ai-pass-agent-3e4f276192b2.json', 
            scopes=SCOPES
        )
    return build('sheets', 'v4', credentials=credentials)

def log_task(task, participants):
    try:
        service = get_service()
        time_stamp = str(datetime.datetime.now())
        participant_str = ", ".join(participants) if participants else "None"
        
        values = [[task, participant_str, time_stamp]]
        body = {'values': values}
        
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A:C",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        return True
    except Exception as e:
        print(f"Sheets Error: {e}")
        return False