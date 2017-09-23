from django.http.response import HttpResponse
from django.utils.encoding import smart_str
from django.views.generic.list import ListView


class DownloadBaseView(ListView):

    def get(self, request, *args, **kwargs):
        queryset = self.model.apply_search_filters(request=request)
        download_data = self.model.prepare_table_data(queryset=queryset)
        download_headers = self.model.get_download_template_headers()
        downloader_class = self.model.get_downloader_class()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
            self.model.get_download_file_name() + ".xlsx")

        downloader = downloader_class(writer=self.model.get_writter_class())
        response = downloader.download(data=download_data, headers=download_headers, response=response)
        if response:
            return response
        return HttpResponse("Download Failed")