from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.contrib import messages
import os
import uuid
from book_rental.libs.uploader.category_uploader import CategoryUploader
from bradmin.views.admin_base_template_view import AdminBaseTemplateView
from generics.libs.reader.excel_file_reader import ExcelFileReader


class AdminCategoryView(TemplateView):
    template_name = "admin/category_master.html"


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