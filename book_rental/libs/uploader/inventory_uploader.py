from django.db import transaction
# from brlogger.models.error_log import ErrorLog


class InventoryUploader(object):
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
                warehouse_code = row[index] if row[index] else None
                index += 1
                book_code = row[index] if row[index] else None
                index += 1
                total = row[index] if row[index] else None
                index += 1
                is_new = row[index] if row[index] else None
                index += 1
                available_for_rent = row[index] if row[index] else None




