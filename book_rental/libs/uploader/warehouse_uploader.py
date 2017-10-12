from django.db import transaction
# from brlogger.models.error_log import ErrorLog
from bauth.models.phone import Phone
from generics.libs.loader.loader import load_model
from logger.models.error_log import ErrorLog


class WarehouseUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        Warehouse = load_model(app_label="ecommerce", model_name="Warehouse")
        self.data = self.data[1:]
        for row in self.data:
            try:
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

                    if not name:
                        ErrorLog.log(url='', stacktrace='Warehouse name must be given. skipping...',
                                     context=Warehouse.__name__)
                        continue

                    if not description:
                        ErrorLog.log(url='', stacktrace='Warehouse description must be given. skipping...',
                                     context=Warehouse.__name__)
                        continue

                    if code:
                        wh_objects = Warehouse.objects.filter(code=code)
                        if wh_objects.exists():
                            wh_object = wh_objects.first()
                        else:
                            ErrorLog.log(url='', stacktrace='Invalid code given. Data %s' % str(row),
                                         context=Warehouse.__name__)
                            continue
                    else:
                        wh_objects = Warehouse.objects.filter(name=str(name))
                        if wh_objects.exists():
                            wh_object = wh_objects.first()
                        else:
                            wh_object = Warehouse()
                    wh_object.name = str(name)
                    wh_object.description = str(description)

                    if contact_no:
                        phones = Phone.objects.filter(number=contact_no)
                        if phones.exists():
                            phone_object = phones.first()
                        else:
                            phone_object = Phone(number=contact_no)
                            phone_object.save()

                        wh_object.contact_id = phone_object.pk

                    if contact_name:
                        wh_object.warehouse_manager = str(contact_name)

                    wh_object.save()
            except Exception as exp:
                ErrorLog.log(url='', stacktrace='Exception Occured. Message: %s' % str(exp),
                             context=Warehouse.__name__)
        return True
                    
                




