from django.views.generic.list import ListView
from bradmin.mixins.admin_action_button_mixin import AdminActionButtonMixin
from bradmin.mixins.admin_list_context_mixin import AdminListContextMixin
from bradmin.mixins.admin_list_data_mixin import AdminListDataMixin
from bradmin.mixins.admin_list_menu_mixin import AdminListMenuMixin
from bradmin.mixins.admin_list_search_mixin import AdminListSearchMixin


class BaseListView(AdminActionButtonMixin, AdminListDataMixin, AdminListSearchMixin,
                   AdminListContextMixin, AdminListMenuMixin, ListView):
    paginate_by = 5

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()
        queryset = self.apply_search_filter(request=self.request, queryset=queryset)
        return queryset
