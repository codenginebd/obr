from django.views.generic.list import ListView


class BaseListView(ListView):
    paginate_by = 20

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_top_menu(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context["tmenu"] = self.get_top_menu()
        context["object_count"] = self.get_queryset().count()
        return context