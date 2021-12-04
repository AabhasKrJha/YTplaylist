import json
from colored import stylize, fg
import os
import pickle

import google.oauth2.credentials

#------------------------------------------------------------------------------

def colorPrint(text):
    def color(data):
        data = stylize(data, fg("green"))
        print(data)
    if type(text) == dict:
        data = json.dumps(text)
    else:
        try:
            data = json.dumps(json.loads(text), indent=2)
        except:
            color(text)
            return

    color(data)

#------------------------------------------------------------------------------

class Credentials :

    def save(credentials):
        with open('token.pickle', 'wb') as f:
            colorPrint('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

    def get():
        credentials = None
        if os.path.exists('token.pickle'):
            colorPrint('Loading Credentials...')
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        return credentials

#------------------------------------------------------------------------------

def credential_object(session_credentials):

    session_credentials = json.loads(session_credentials)
    
    credentials = google.oauth2.credentials.Credentials(
            session_credentials["token"],
            refresh_token = session_credentials["refresh_token"],
            token_uri = session_credentials["token_uri"],
            client_id = session_credentials["client_id"],
            client_secret = session_credentials["client_secret"],
            scopes = session_credentials["scopes"])
    
    return credentials