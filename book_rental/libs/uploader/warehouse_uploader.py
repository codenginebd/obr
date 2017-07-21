from django.db import transaction
# from brlogger.models.error_log import ErrorLog


class WarehouseUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
            with transaction.atomic():
                index = 0
                code = row[index].strip() if row[index] else None
                index += 1
                name = row[index] if row[index] else None
                index += 1
                description = row[index] if row[index] else None
                index += 1
                contact_name = row[index] if row[index] else None
                index += 1
                contact_no = row[index] if row[index] else None




