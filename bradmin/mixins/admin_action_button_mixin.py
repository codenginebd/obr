from django.urls.base import reverse, resolve


class AdminActionButtonMixin(object):
    def show_upload(self):
        return self.model.show_upload()

    def show_download(self):
        return self.model.show_download()

    def show_download_template(self):
        return self.model.show_download_template()

    def show_create(self):
        return self.model.show_create()

    def show_edit(self):
        return self.model.show_edit()

    def show_delete(self):
        return self.model.show_delete()

    def show_activate(self):
        return self.model.show_activate()

    def show_deactivate(self):
        return self.model.show_deactivate()

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

    def get_create_link(self):
        return self.model.get_create_link()

    def get_edit_link_name(self):
        return self.model.get_edit_link_name()

    def get_edit_link(self, object_id):
        return self.model.get_edit_link(object_id=object_id)

    def get_delete_link(self):
        return self.model.get_delete_link()

    def get_activate_link(self):
        return self.model.get_activate_link()

    def get_deactivate_link(self):
        return self.model.get_deactivate_link()