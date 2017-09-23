from bradmin.views.base_list_view import BaseListView
from logger.models.error_log import ErrorLog


class AdminLogView(BaseListView):
    template_name = "admin/errorlog_list.html"
    model = ErrorLog