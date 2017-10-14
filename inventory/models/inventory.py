from django.db import models
from django.urls.base import reverse

from book_rental.libs.downloader.inventory_downloader import InventoryDownloader
from book_rental.libs.uploader.inventory_uploader import InventoryUploader
from ecommerce.models.sales.warehouse import Warehouse
from generics.libs.loader.loader import load_model
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.models.base_entity import BaseEntity


class Inventory(BaseEntity):
    product_id = models.BigIntegerField(default=0)
    product_model = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse)
    stock = models.BigIntegerField(default=0)
    available_for_buy = models.BooleanField(default=False)
    available_for_rent = models.BooleanField(default=False)
    available_for_sale = models.BooleanField(default=False)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50) # COL, ORI, ECO #Color, Original and Economy
    comment = models.TextField(null=True)

    @property
    def print_type_full_name(self):
        if self.print_type == 'ORI':
            return "Original"
        elif self.print_type == 'COL':
            return "Color"
        elif self.print_type == 'ECO':
            return "Economy"

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def show_upload(cls):
        return True

    @classmethod
    def show_download(cls):
        return True

    @classmethod
    def show_download_template(cls):
        return True

    @classmethod
    def show_activate(cls):
        return True

    @classmethod
    def show_deactivate(cls):
        return True

    @classmethod
    def show_delete(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_inventory_create_view")

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_inventory_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_inventory_edit_link_view"

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_inventory_details_view", kwargs={"pk": object_id})

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_inventory_upload_view")

    @classmethod
    def get_download_link(cls):
        return reverse("admin_inventory_download_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_inventory_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_inventory_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_inventory_delete_view")

    @classmethod
    def get_downloader_class(cls):
        return InventoryDownloader

    @classmethod
    def get_uploader_class(cls):
        return InventoryUploader

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_download_headers(cls):
        return ["Id", "code", "Product", "Warehouse", "Is New", "Printing Type", "Stock",
                "Available for Buy", "Available for Sale", "Available for Rent"]

    @classmethod
    def prepare_download_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.get_product_name(), q_object.warehouse.name,
                    "Yes" if q_object.is_new == 1 else "No", q_object.print_type_full_name, q_object.stock,
                    "Yes" if q_object.available_for_buy else "No",
                    "Yes" if q_object.available_for_sale else "No",
                    "Yes" if q_object.available_for_rent else "No"
                ]
            ]
        return data

    @classmethod
    def get_download_template_headers(cls):
        return [
            "Code", "Warehouse Code", "Book Code", "Is New?", "Print Type", "Current Stock", "New Stock",
            "Available For Sale","Available For Rent", "Available For Buy",
            "Supplier Name", "Address 1", "Address2", "Address3", "Address4", "Phone1", "Phone2", "Note"
        ]

    @classmethod
    def get_download_file_name(cls):
        return "Inventory List"

    @classmethod
    def prepare_download_template_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.code, q_object.warehouse.code ,q_object.get_product_code(), "1" if q_object.is_new == 1 else "0",
                    q_object.print_type, q_object.stock, "0", "1" if q_object.available_for_sale else "0",
                    "1" if q_object.available_for_rent else "0", "1" if q_object.available_for_buy else "0",
                    "", "", "", "", "", "", "", ""

                ]
            ]
        return data

    def get_product(self):
        Book = load_model(app_label="book_rental", model_name="Book")
        if self.product_model == Book.__name__:
            return Book.objects.get(pk=self.product_id)

    def get_product_name(self):
        product = self.get_product()
        if product:
            return product.title

    def get_product_code(self):
        product = self.get_product()
        if product:
            return product.code

    @classmethod
    def get_table_headers(self):
        return ["Id", "code", "Product", "Warehouse", "Is New", "Printing Type", "Stock",
                "Available for Buy", "Available for Sale", "Available for Rent", "Is Active", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.get_product_name(), q_object.warehouse.name,
                    "Yes" if q_object.is_new == 1 else "No", q_object.print_type_full_name, q_object.stock,
                    "Yes" if q_object.available_for_buy else "No",
                    "Yes" if q_object.available_for_sale else "No",
                    "Yes" if q_object.available_for_rent else "No", "Yes" if q_object.is_active else "No",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    @classmethod
    def get_search_by_options(cls):
        search_by_options = super(Inventory, cls).get_search_by_options()
        search_by_options += [
            ("By Product", "product"),
            ("By Warehouse", "warehouse"),
            ("Is New", "is_new"),
            ("By Print Type", "print_type"),
            ("By Stock", "stock"),
            ("By Sale Available", "by_sale_available"),
            ("By Rent Available", "by_rent_available"),
            ("By Buy Available", "by_buy_available")
        ]
        return search_by_options