import os
from django.conf import settings
from django.core.files.storage import Storage
from dropbox import Dropbox
from dropbox.files import WriteMode
from decouple import config


class DropboxMediaFileStorage(Storage):
    def __init__(self, access_token=None):
        if access_token is None:
            access_token = config("DROPBOX_ACCESS_TOKEN", default="")
        self.client = Dropbox(access_token)

    def _save(self, name, content):
        path = os.path.join(settings.MEDIA_ROOT, name)
        with content.open('rb') as f:
            self.client.files_upload(f.read(), "/" + name, mode=WriteMode("overwrite"))
        return name

    def url(self, name):
        return self.client.files_get_temporary_link("/" + name).link
