import os
from django.conf import settings
from django.core.files.storage import Storage
from dropbox import Dropbox, DropboxOAuth2Flow
from dropbox.files import WriteMode
from decouple import config
import requests

class DropboxMediaFileStorage(Storage):
    def __init__(self):
        self.client = self.get_dropbox_client()

    def get_dropbox_client(self):
        # Check if access token is available
        access_token = self.get_access_token()
        if access_token:
            return Dropbox(access_token)

        return None

    def get_access_token(self):
        # Check if access token is available
        access_token = config("DROPBOX_ACCESS_TOKEN", default=None)
        if access_token:
            return access_token

        # Your Dropbox app credentials
        APP_KEY = config("DROPBOX_APP_KEY", default="")
        APP_SECRET = config("DROPBOX_APP_SECRET", default="")
        REDIRECT_URI = config("DROPBOX_REDIRECT_URI", default="")
        CSRF_TOKEN = config("DROPBOX_CSRF_TOKEN", default="")

        # Use the refresh token to get a new access token
        refresh_token = config("DROPBOX_REFRESH_TOKEN", default="")
        if refresh_token:
            access_token = self.refresh_access_token(refresh_token, APP_KEY, APP_SECRET)
            return access_token

        return None

    def refresh_access_token(self, refresh_token, app_key, app_secret):
        token_exchange_url = "https://api.dropbox.com/oauth2/token"
        refresh_payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": app_key,
            "client_secret": app_secret
        }
        refresh_response = requests.post(token_exchange_url, data=refresh_payload)
        refresh_response_data = refresh_response.json()
        new_access_token = refresh_response_data.get('access_token')
        return new_access_token

    def _save(self, name, content):
        path = os.path.join(settings.MEDIA_ROOT, name)
        with content.open('rb') as f:
            self.client.files_upload(f.read(), "/" + name, mode=WriteMode("overwrite"))
        return name

    def url(self, name):
        return self.client.files_get_temporary_link("/" + name).link
