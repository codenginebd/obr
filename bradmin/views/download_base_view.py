import os
import uuid

from django.http.response import HttpResponse
from django.utils.encoding import smart_str
from django.views.generic.list import ListView


class DownloadBaseView(ListView):

    def generate_random_file_name(self):
        return str(uuid.uuid4())

    def get(self, request, *args, **kwargs):
        queryset = self.model.apply_search_filters(request=request)
        download_data = self.model.prepare_table_data(queryset=queryset)
        download_headers = self.model.get_download_template_headers()
        downloader_class = self.model.get_downloader_class()
        temp_file_name = self.generate_random_file_name()
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        file_path = PROJECT_ROOT + '/book_rental/management/commands/downloads/%s.xlsx' % temp_file_name
        downloader = downloader_class(file_name=file_path, writer=self.model.get_writter_class())
        path_to_file = downloader.download(data=download_data, headers=download_headers)
        if path_to_file:
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(self.model.get_download_file_name()+".xlsx")
            response['X-Sendfile'] = smart_str(path_to_file)
            return response
        return HttpResponse("Download Failed")