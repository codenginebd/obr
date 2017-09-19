from django.views.generic.list import ListView


class BaseListView(ListView):

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

    def get_headers(self):
        return []

    def get_table_data(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context["breadcumb"] = self.get_breadcumb()
        context["left_menu_items"] = self.get_left_menu_items()
        context["headers"] = self.get_headers()
        context["table_data"] = self.get_table_data()
        return context