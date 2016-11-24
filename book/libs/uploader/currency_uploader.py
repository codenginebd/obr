from django.db import transaction
from br_blogger.models.error_log import ErrorLog

class CurrencyUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
            pass