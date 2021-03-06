from django.db import transaction
from ecommerce.models.sales.warehouse import Warehouse
from enums import InventoryTXNType
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
                    product_code = row[index] if row[index] else None
                    index += 1
                    is_new = 1 if row[index] else 0
                    index += 1
                    printing_type = row[index] if row[index] else None
                    index += 1
                    current_stock = row[index] if row[index] else 0
                    index += 1
                    new_stock = row[index] if row[index] else 0
                    index += 1
                    available_for_sale = row[index] if row[index] else 0
                    index += 1
                    available_for_rent = row[index] if row[index] else 0
                    index += 1
                    available_for_buy = row[index] if row[index] else 0
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
                    note = row[index]

                    if any([ not item for item in [ warehouse_code, product_code, printing_type ] ]):
                        ErrorLog.log(url='', stacktrace='Book Upload missing data: %s. Skipping...' % str(row),
                                     context=Inventory.__name__)
                        continue

                    if not int(new_stock) or int(new_stock) < 0:
                        ErrorLog.log(url='', stacktrace='New stock must be greater than 0. Provided: %s. Skipping...' % str(new_stock),
                                     context=Inventory.__name__)

                    warehouse_object = None
                    warehouse_objects = Warehouse.objects.filter(code=str(warehouse_code))
                    if warehouse_objects.exists():
                        warehouse_object = warehouse_objects.first()
                    else:
                        ErrorLog.log(url='', stacktrace='Missing warehouse in inventory upload. data: %s. Skipping...' % str(warehouse_code),
                                     context=Inventory.__name__)
                        continue

                    book_object = None
                    book_objects = Book.objects.filter(code=str(product_code))
                    if book_objects.exists():
                        book_object = book_objects.first()
                    else:
                        ErrorLog.log(url='',
                                     stacktrace='Missing book in inventory upload. data: %s. Skipping...' % str(product_code),
                                     context=Inventory.__name__)
                        continue

                    try:
                        current_stock = int(current_stock)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid current_stock. Number expected. data: %s. Skipping...' % str(current_stock),
                                     context=Inventory.__name__)
                        continue

                    try:
                        new_stock = int(new_stock)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid new_stock. Number expected. data: %s. Skipping...' % str(
                                         new_stock),
                                     context=Inventory.__name__)
                        continue

                    try:
                        is_new = int(is_new)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid Is New. 1 or 0 expected. data: %s. Skipping...' % str(is_new),
                                     context=Inventory.__name__)
                        continue

                    if is_new == 1:
                        is_new = True
                    elif is_new == 0:
                        is_new = False

                    try:
                        available_for_sale = int(available_for_sale)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid available_for_sale. 1 or 0 expected. data: %s. Skipping...' % str(
                            available_for_sale),
                                     context=Inventory.__name__)
                        continue

                    try:
                        available_for_rent = int(available_for_rent)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid available_for_rent. 1 or 0 expected. data: %s. Skipping...' % str(
                                         available_for_rent),
                                     context=Inventory.__name__)
                        continue

                    try:
                        available_for_buy = int(available_for_buy)
                    except:
                        ErrorLog.log(url='',
                                     stacktrace='Invalid available_for_buy. 1 or 0 expected. data: %s. Skipping...' % str(
                                         available_for_buy),
                                     context=Inventory.__name__)
                        continue

                    if available_for_sale == 1:
                        available_for_sale = True
                    elif available_for_sale == 0:
                        available_for_sale = False

                    if available_for_rent == 1:
                        available_for_rent = True
                    elif available_for_rent == 0:
                        available_for_rent = False

                    if available_for_buy == 1:
                        available_for_buy = True
                    elif available_for_buy == 0:
                        available_for_buy = False

                    if printing_type not in [ 'COL', 'ORI', 'ECO' ]:
                        ErrorLog.log(url='',
                                     stacktrace='Printing type must be in COL, ORI, ECO. data: %s. Skipping...' % str(
                                         printing_type),
                                     context=Inventory.__name__)
                        continue

                    if code:
                        inventory_objects = Inventory.objects.filter(code=code)
                        if inventory_objects.exists():
                            inventory_object = inventory_objects.first()
                        else:
                            ErrorLog.log(url='',
                                         stacktrace='Invalid inventory code. data: %s. Skipping...' % str(code),
                                         context=Inventory.__name__)
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

                    stock = inventory_object.stock + new_stock

                    inventory_object.product_id = book_object.pk
                    inventory_object.product_model = book_object.__class__.__name__
                    inventory_object.warehouse_id = warehouse_object.pk
                    inventory_object.stock = stock
                    inventory_object.available_for_sale = available_for_sale
                    inventory_object.available_for_rent = available_for_rent
                    inventory_object.available_for_buy = available_for_buy
                    inventory_object.is_new = is_new
                    inventory_object.print_type = printing_type
                    inventory_object.comment = note
                    inventory_object.save()

                    supplier_object = None
                    if supplier_name:
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
                            supplier_object.notes = str(note)
                            supplier_object.save()
                    inventory_transaction = InventoryTransaction()
                    inventory_transaction.transaction_type = InventoryTXNType.STOCK_IN.value
                    inventory_transaction.qty = new_stock
                    if supplier_object:
                        inventory_object.supplier_id = supplier_object.pk
                    inventory_transaction.warehouse_id = warehouse_object.pk
                    inventory_transaction.product_id = book_object.pk
                    inventory_transaction.product_model = book_object.__class__.__name__
                    inventory_transaction.is_new = is_new
                    inventory_transaction.print_type = printing_type
                    inventory_transaction.save()
            except Exception as exp:
                ErrorLog.log(url='',
                             stacktrace='Exception Occured. Message: %s. Skipping...' % str(exp),
                             context=Inventory.__name__)
        return True





