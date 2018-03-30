from django.db import models
from django.urls.base import reverse

from bauth.models.phone import Phone
from book_rental.libs.downloader.warehouse_downloader import WarehouseDownloader
from book_rental.libs.uploader.warehouse_uploader import WarehouseUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.models.base_entity import BaseEntity


class Warehouse(BaseEntity):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(Phone, null=True, on_delete=models.CASCADE)
    warehouse_manager = models.CharField(max_length=200, blank=True, null=True)

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
        return reverse("admin_warehouse_create_view")

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_warehouse_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_warehouse_edit_link_view"

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_warehouse_upload_view")

    @classmethod
    def get_download_link(cls):
        return reverse("admin_warehouse_download_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_warehouse_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_warehouse_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_warehouse_delete_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_warehouse_details_view", kwargs={"pk": object_id})

    @classmethod
    def get_uploader_class(cls):
        return WarehouseUploader

    @classmethod
    def get_downloader_class(cls):
        return WarehouseDownloader

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Name", "Is Active", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, "Yes" if q_object.is_active else "No",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    @classmethod
    def get_download_headers(cls):
        return ["Code", "Name", "Description", "Is Active"]

    @classmethod
    def prepare_download_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.code, q_object.name, q_object.description, "Yes" if q_object.is_active else "No"
                ]
            ]
        return data

    @classmethod
    def get_download_file_name(cls):
        return "Warehouse List"

    @classmethod
    def get_download_template_headers(cls):
        return ["Code", "Name", "Description", "Contact Name", "Contact No"]

    @classmethod
    def prepare_download_template_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.code, q_object.name, q_object.description,
                    q_object.warehouse_manager if q_object.warehouse_manager else "",
                    q_object.contact.number if q_object.contact else ""
                ]
            ]
        return data

