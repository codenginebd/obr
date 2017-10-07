from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from logger.models.error_log import ErrorLog


class AdminListContextMixin(object):
    def get_extra_context(self, request, queryset):
        return {}

    def get_page_title(self):
        return "BDReads.com"

    def get_search_param_context(self, request):
        return request.GET.get("context", "")

    def get_context_data(self, **kwargs):
        context = super(AdminListContextMixin, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        total_count = queryset.count()
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        self.object_list = object_list
        context["page_title"] = self.get_page_title()
        context["show_upload"] = self.show_upload()
        context["show_download"] = self.show_download()
        context["show_download_template"] = self.show_download_template()
        context["show_create"] = self.show_create()
        context["show_edit"] = self.show_edit()
        context["show_delete"] = self.show_delete()
        context["show_activate"] = self.show_activate()
        context["show_deactivate"] = self.show_deactivate()
        context["search_by_options"] = self.get_search_by_options()
        context["advanced_search_options"] = self.get_advanced_search_options()
        context["search_by"] = self.collect_search_by(request=self.request)
        context["search_keyword"] = self.collect_search_keyword(request=self.request)
        context["search_advanced_params"] = self.collect_search_advanced_params(request=self.request)
        context["search_param_url"] = self.collect_search_params(request=self.request)
        context["search_param_context"] = self.get_search_param_context(request=self.request)
        context["upload_link"] = self.get_upload_link()
        context["download_link"] = self.get_download_link()
        context["download_template_link"] = self.get_download_template_link()
        context["create_link"] = self.get_create_link()
        context["edit_link_name"] = self.get_edit_link_name()
        context["delete_link"] = self.get_delete_link()
        context["activate_link"] = self.get_activate_link()
        context["deactivate_link"] = self.get_deactivate_link()
        context["upload_redirect"] = self.get_upload_redirect_url(request=self.request)
        context["breadcumb"] = self.get_breadcumb(request=self.request)
        context["left_menu_items"] = self.get_left_menu_items()
        context["headers"] = self.get_table_headers()
        context["table_data"] = self.prepare_table_data(queryset=object_list)
        context["total_count"] = total_count
        extra_context = self.get_extra_context(request=self.request, queryset=object_list)
        for key, item in extra_context.items():
            if key not in context.keys():
                context[key] = item
            else:
                ErrorLog.log(url='',
                             stacktrace='%s cannot be used as key as it is already in use in the parent context',
                             context='%s' % self.model.__name__)
        return context