from flask import Blueprint
from flask import session, redirect, jsonify
import json

import google.oauth2.credentials
from googleapiclient.discovery import build

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/")
def dashboard():

    """User Dashboard"""

    if "credentials" not in session:
        return redirect("/auth")

    else:
        session_credentials = json.loads(session['credentials'])

        credentials = google.oauth2.credentials.Credentials(
            session_credentials["token"],
            refresh_token = session_credentials["refresh_token"],
            token_uri = session_credentials["token_uri"],
            client_id = session_credentials["client_id"],
            client_secret = session_credentials["client_secret"],
            scopes = session_credentials["scopes"])

        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'

        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        request = youtube.channels().list(mine=True, part='snippet')
        response = request.execute()

        # Save credentials back to session in case access token was refreshed.
        session['credentials'] = credentials.to_json()

        return jsonify(**response)

