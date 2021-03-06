from django.urls.base import reverse, resolve

from bradmin.enums import ViewAction


class AdminActionButtonMixin(object):
    def show_upload(self):
        return self.model.show_upload()
        
    def show_upload_as(self):
        return self.model.show_upload_as()

    def show_download(self):
        return self.model.show_download()
        
    def show_download_as(self):
        return self.model.show_download_as()

    def show_download_template(self):
        return self.model.show_download_template()
        
    def show_download_template_as(self):
        return self.model.show_download_template_as()

    def show_create(self):
        return self.model.show_create()
        
    def show_create_as(self):
        return self.model.show_create_as()

    def show_edit(self):
        return self.model.show_edit()
        
    def show_edit_as(self):
        return self.model.show_edit_as()

    def show_delete(self):
        return self.model.show_delete()
        
    def show_delete_as(self):
        return self.model.show_delete_as()

    def show_activate(self):
        return self.model.show_activate()
        
    def show_activate_as(self):
        return self.model.show_activate_as()

    def show_deactivate(self):
        return self.model.show_deactivate()
        
    def show_deactivate_as(self):
        return self.model.show_deactivate_as()

    def show_approve(self):
        return self.model.show_approve()
        
    def show_approve_as(self):
        return self.model.show_approve_as()

    def show_reject(self):
        return self.model.show_reject()
        
    def show_reject_as(self):
        return self.model.show_reject_as()

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

    def get_view_actions(self):
        actions = self.model.get_view_actions()
        context = {}
        for key, link in actions.items():
            if key.value == ViewAction.EDIT_NAME:
                if link:
                    context["edit_link_name"] = link
            else:
                if link:
                    context["show_%s" % key.value] = True
                    context["%s_link" % key.value] = link
        return context