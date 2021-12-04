from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build

#---------------------------------------------------------------------------------------

from YTplaylist.common_fxn import colorPrint, Credentials

#---------------------------------------------------------------------------------------
   
# os.system("source .env")
# api_key = os.environ.get("API_KEY")

credentials = Credentials.get()

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:

        colorPrint('Credentials Expired, Refreshing Access Token...')
        credentials.refresh(Request())
        Credentials.save(credentials)

    else:

        colorPrint('Fetching New Tokens...')

        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['https://www.googleapis.com/auth/youtube.readonly']
        )
        flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
        credentials = flow.credentials

        Credentials.save(credentials)

youtube = build("youtube", "v3", credentials=credentials)

request = youtube.playlistItems().list(
        part="status",
        id="PLtCKS3CuBDYV_Vyl1ZH2Je8gSdXfQf4e3"
    )

response = request.execute()

# colorPrint(credentials.to_json())