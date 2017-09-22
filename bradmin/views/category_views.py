from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.contrib import messages
import os
import uuid
from book_rental.libs.uploader.category_uploader import CategoryUploader
from bradmin.views.admin_base_template_view import AdminBaseTemplateView
from bradmin.views.base_list_view import BaseListView
from ecommerce.models.sales.category import ProductCategory
from generics.libs.reader.excel_file_reader import ExcelFileReader


class AdminCategoryView(TemplateView):
    template_name = "admin/category_master.html"


class AdminCategoryListView(BaseListView):
    model = ProductCategory
    template_name = "admin/category_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": "admin_category_view",
            "Upload/Download": "admin_category_upload_view"
        }

    def get_headers(self):
        return [
            "ID", "Code", "Name(English)", "Name(Bangla)", "Active?", "Show Bangla", "Parent", "Details"
        ]

    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, q_object.name_2, q_object.is_active,
                    True if q_object.show_name_2 else False,
                    q_object.parent.name if q_object.parent else "-",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data


class AdminCategoryUploadView(AdminBaseTemplateView):
    template_name = "admin/category_upload.html"

    def get_left_menu_items(self):
        return {
            "Create": "/",
            "Upload": "/",
            "Upload Logs": ""
        }

    def get_content_data(self):
        return {

        }

    def post(self, request, *args, **kwargs):
        attachment = request.FILES.get('uploaded_file')
        if not attachment:
            messages.add_message(request, messages.INFO, 'File is required')
            return HttpResponseRedirect(reverse("admin_category_upload_view"))

        file_name = str(request.user.id) + "-" + str(uuid.uuid4()) + "." + attachment._name[
                                                                           attachment._name.rindex(".") + 1:]
        file_write_path = os.path.join(settings.MEDIA_TEMP_PATH, file_name)
        with open(os.path.join(settings.MEDIA_TEMP_PATH, file_name), 'wb+') as destination:
            for chunk in attachment.chunks():
                destination.write(chunk)

        excel_reader = ExcelFileReader(file_name=file_write_path, sheet_name='Sheet1')
        data = excel_reader.get_data()
        category_uploader = CategoryUploader(data=data)
        category_uploader.handle_upload()

        os.remove(file_write_path)
        messages.add_message(request, messages.INFO, 'File uploaded successfully')
        return HttpResponseRedirect(reverse("admin_category_upload_view"))