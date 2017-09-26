from django.urls.base import reverse, resolve


class AdminActionButtonMixin(object):
    def show_upload(self):
        return False

    def show_download(self):
        return False

    def show_download_template(self):
        return False

    def show_edit(self):
        return False

    def show_delete(self):
        return False

    def show_activate(self):
        return False

    def show_deactivate(self):
        return False

    def get_upload_link(self):
        return self.model.get_upload_link()

    def get_upload_redirect_url(self, request):
        return reverse(resolve(request.path_info).url_name)

    def get_download_link(self):
        return self.model.get_download_link()

    def get_download_template_link(self):
        download_link = self.get_download_link()
        if download_link:
            return download_link + "?template=1"
        return download_link

    def get_delete_link(self):
        return self.model.get_delete_link()

    def get_activate_link(self):
        return self.model.get_activate_link()

    def get_deactivate_link(self):
        return self.model.get_deactivate_link()