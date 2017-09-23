import os
import uuid
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, resolve
from django.views.generic.list import ListView
from django.contrib import messages


class UploadBaseView(ListView):

    def post(self, request, *args, **kwargs):
        attachment = request.FILES.get('uploaded_file')
        upload_redirect = request.POST.get("upload_redirect")
        if not attachment:
            messages.add_message(request, messages.INFO, 'File is required')
            if upload_redirect:
                return HttpResponseRedirect(upload_redirect)
            else:
                return HttpResponseRedirect(reverse(resolve(request.path_info).url_name))

        file_name = str(request.user.id) + "-" + str(uuid.uuid4()) + "." + attachment._name[
                                                                           attachment._name.rindex(".") + 1:]
        file_write_path = os.path.join(settings.MEDIA_TEMP_PATH, file_name)
        with open(file_write_path, 'wb+') as destination:
            for chunk in attachment.chunks():
                destination.write(chunk)

        reader_class = self.model.get_reader_class()
        reader = reader_class(file_name=file_write_path, sheet_name='Sheet1')
        data = reader.get_data()
        uploader_class = self.model.get_uploader_class()
        category_uploader = uploader_class(data=data)
        uploaded = category_uploader.handle_upload()
        os.remove(file_write_path)
        if uploaded:
            messages.add_message(request, messages.INFO, 'File uploaded successfully')
        else:
            messages.add_message(request, messages.INFO, 'File upload failed')

        if upload_redirect:
            return HttpResponseRedirect(upload_redirect)
        else:
            return HttpResponseRedirect(reverse(resolve(request.path_info).url_name))