from django.db import transaction
from ecommerce.models.sales.warehouse import Warehouse
from generics.libs.loader.loader import load_model
from inventory.models.inventory_transaction import InventoryTransaction
from inventory.models.product_supplier import ProductSupplier
from logger.models.error_log import ErrorLog


class InventoryUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        Book = load_model(app_label="book_rental", model_name="Book")
        Inventory = load_model(app_label="inventory", model_name="Inventory")
        self.data = self.data[1:]
        for row in self.data:
            try:
                with transaction.atomic():
                    index = 0
                    code = row[index].strip() if row[index] else None
                    index += 1
                    warehouse_code = row[index] if row[index] else None
                    index += 1
                    book_code = row[index] if row[index] else None
                    index += 1
                    total = row[index]
                    index += 1
                    is_new = 1 if row[index] else 0
                    index += 1
                    available_for_rent = 1 if row[index] else 0
                    index += 1
                    printing_type = row[index] if row[index] else None
                    index += 1
                    supplier_name = row[index]
                    index += 1
                    address1 = row[index]
                    index += 1
                    address2 = row[index]
                    index += 1
                    address3 = row[index]
                    index += 1
                    address4 = row[index]
                    index += 1
                    phone1 = row[index]
                    index += 1
                    phone2 = row[index]
                    index += 1
                    notes = row[index]

                    if any([ not item for item in [ warehouse_code, book_code, available_for_rent, printing_type ] ]):
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Book Upload missing data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    warehouse_object = None
                    warehouse_objects = Warehouse.objects.filter(code=str(warehouse_code))
                    if warehouse_objects.exists():
                        warehouse_object = warehouse_objects.first()
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Missing warehouse in inventory upload. data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    book_object = None
                    book_objects = Book.objects.filter(code=str(book_code))
                    if book_objects.exists():
                        book_object = book_objects.first()
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Missing book in inventory upload. data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    try:
                        total = int(total)
                    except:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid total. Number expected. data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    try:
                        is_new = int(is_new)
                    except:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid Is New. 1 or 0 expected. data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    if is_new == 1:
                        is_new = True
                    elif is_new == 0:
                        is_new = False

                    try:
                        available_for_rent = int(available_for_rent)
                    except:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid available_for_rent. 1 or 0 expected. data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue

                    if available_for_rent == 1:
                        available_for_rent = True
                    elif available_for_rent == 0:
                        available_for_rent = False

                    if printing_type not in [ 'COL', 'ORI', 'ECO' ]:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Printing type must be in COL, ORI, ECO. data: %s. Skipping...' % str(
                            row)
                        error_log.save()
                        continue

                    if code:
                        inventory_objects = Inventory.objects.filter(code=code)
                        if inventory_objects.exists():
                            inventory_object = inventory_objects.first()
                        else:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Invalid inventory code. data: %s. Skipping...' % str(
                                row)
                            error_log.save()
                            continue
                    else:
                        inventory_objects = Inventory.objects.filter(warehouse_id=warehouse_object.pk,
                                                                     product_id=book_object.pk,
                                                                     product_model=book_object.__class__.__name__,
                                                                     is_new=is_new,
                                                                     print_type=printing_type,
                                                                     available_for_rent=available_for_rent)
                        if inventory_objects.exists():
                            inventory_object = inventory_objects.first()
                        else:
                            inventory_object = Inventory()

                    inventory_object.product_id = book_object.pk
                    inventory_object.product_model = book_object.__class__.__name__
                    inventory_object.warehouse_id = warehouse_object.pk
                    inventory_object.stock = total
                    inventory_object.available_for_rent = available_for_rent
                    inventory_object.is_new = is_new
                    inventory_object.print_type = printing_type
                    inventory_object.comment = 'Inventory upload via xls file'
                    inventory_object.save()

                    supplier_objects = ProductSupplier.objects.filter(name=str(supplier_name))
                    if supplier_objects.exists():
                        supplier_object = supplier_objects.first()
                    else:
                        supplier_object = ProductSupplier()
                        supplier_object.name = str(supplier_name)
                        supplier_object.address_line1 = str(address1)
                        supplier_object.address_line2 = str(address2)
                        supplier_object.address_line3 = str(address3)
                        supplier_object.address_line4 = str(address4)
                        supplier_object.phone_number1 = str(phone1)
                        supplier_object.phone_number2 = str(phone2)
                        supplier_object.notes = str(notes)
                        supplier_object.save()

                    inventory_transaction = InventoryTransaction()
                    inventory_transaction.transaction_type = 'STOCK_IN'
                    inventory_transaction.qty = total
                    inventory_transaction.counter_part_id = supplier_object.pk
                    inventory_transaction.counter_part_model = supplier_object.__class__.__name__
                    inventory_transaction.product_id = book_object.pk
                    inventory_transaction.product_model = book_object.__class__.__name__
                    inventory_transaction.is_new = is_new
                    inventory_transaction.print_type = printing_type
                    inventory_transaction.save()

                    print("Done!")
            except Exception as exp:
                print("Exception")
                print(str(exp))






