from flask import Blueprint

from flask import redirect,url_for
from flask import session
from flask import request

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials

import requests

from YTplaylist.common_fxn import colorPrint, credential_object

import json

#--------------------------------------------------------------------------------------

# authentiation(OAuth) Blueprint
bp = Blueprint("auth", __name__, url_prefix = "/auth")

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

#--------------------------------------------------------------------------------------

@bp.route("/")
def index():

    """auth API endpoint for OAuth implementation"""

    # check existing credentials
    # if valid credentails are not available, refresh or login 

    if "credentials" not in session:
        colorPrint("Credentials not found, redirecting to /auth/authorisation ....")
        # redirect to /auth/login for google OAuth login
        return redirect("authorisation")

    else:

        colorPrint("Credentials found, checking validity ....")

        session_credentials = session['credentials']
        credentials = credential_object(session_credentials)

        if not credentials or not credentials.valid:

            if credentials and credentials.expired and credentials.refresh_token:

                # if credentails are present in session
                # and if credentaions are expired
                # and if previous refresh/access token in available
                
                colorPrint('Credentials Expired, Refreshing Access Token...')
                credentials.refresh(Request())

                session['credentials'] = credentials.to_json()
                return redirect(url_for("dashboard.dashboard"))

        else:
            return redirect(url_for("dashboard.dashboard"))
        

#--------------------------------------------------------------------------------------

@bp.route("/authorisation")
def authorisation():

    """subroute for /auth
       for stting state key in session
    """

    # if credentails valid, only then this auth process will occur

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)

#--------------------------------------------------------------------------------------

@bp.route("/oauth2callback")
def oauth2callback():

    state = session['state']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url.replace("http", "https")
    colorPrint(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials.to_json()
    colorPrint(credentials)
    session['credentials'] = credentials

    return redirect(url_for('dashboard.dashboard'))
    
#--------------------------------------------------------------------------------------

@bp.route("/revoke")
def revoke():

    """subroute for /auth
       for clearing sessions and revoking credentials
    """

    if 'credentials' not in session:
        return ('You need to authorize before trying revoke credentials.')

    else:

        token = json.loads(session['credentials'])['token']

        # revoke credentials
        revoke = requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': token},
            headers = {'content-type': 'application/x-www-form-urlencoded'}
        )

        status_code = getattr(revoke, 'status_code')

        # remove sessions
        del session['credentials']

        if status_code == 200:
            return('Credentials successfully revoked')
        else:
            return('An error occurred')

        