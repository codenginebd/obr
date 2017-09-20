from django.views.generic.list import ListView


class BaseListView(ListView):
    paginate_by = 15

    def apply_filter(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()
        queryset = self.apply_filter(queryset=queryset)
        return queryset

    def get_breadcumb(self):
        return []

    def get_left_menu_items(self):
        return {}

    def get_table_headers(self):
        return []

    def prepare_table_data(self, queryset):
        return []
        
    def get_extra_context(self, request, queryset):
        return {}

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
        context['list_exams'] = file_exams
        context["breadcumb"] = self.get_breadcumb()
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