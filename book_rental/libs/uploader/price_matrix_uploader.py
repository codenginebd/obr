import os
from django.conf import settings
from django.db import transaction
from datetime import datetime
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class PriceMatrixUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        self.data = self.data[1:]
        for row in self.data:
            with transaction.atomic():
                pass