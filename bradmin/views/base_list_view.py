from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic.list import ListView
from django.core.urlresolvers import resolve
from logger.models.error_log import ErrorLog


class BaseListView(ListView):
    paginate_by = 15

    def apply_filter(self, request, queryset):
        return queryset.model.apply_search_filters(request=request, queryset=queryset)

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()
        queryset = self.apply_filter(request=self.request, queryset=queryset)
        return queryset

    def get_breadcumb(self, request):
        return []

    def get_left_menu_items(self):
        return {}

    def get_table_headers(self):
        return self.model.get_table_headers()

    def prepare_table_data(self, queryset):
        return self.model.prepare_table_data(queryset=queryset)
        
    def get_extra_context(self, request, queryset):
        return {}

    def get_upload_link(self):
        return self.model.get_upload_link()

    def get_upload_redirect_url(self, request):
        return resolve(request.path_info).url_name

    def get_search_by_options(self):
        return self.model.get_search_by_options()

    def get_advanced_search_options(self):
        return self.model.get_advanced_search_options()

    def get_download_link(self):
        return self.model.get_download_link()

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        self.object_list = object_list
        context["search_by_options"] = self.get_search_by_options()
        context["advanced_search_options"] = self.get_advanced_search_options()
        context["upload_link"] = self.get_upload_link()
        context["download_link"] = self.get_download_link()
        context["upload_redirect"] = self.get_upload_redirect_url(request=self.request)
        context["breadcumb"] = self.get_breadcumb(request=self.request)
        context["left_menu_items"] = self.get_left_menu_items()
        context["headers"] = self.get_headers()
        context["table_data"] = self.prepare_table_data(queryset=object_list)
        extra_context = self.get_extra_context(request=self.request, queryset=object_list)
        for key, item in extra_context.items():
            if key not in context.keys():
                context[key] = item
            else:
                ErrorLog.log(url='', stacktrace='%s cannot be used as key as it is already in use in the parent context', context='%s' % self.model.__name__)
        return context