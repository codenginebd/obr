class AdminListMenuMixin(object):
    def get_breadcumb(self, request):
        return []

    def get_left_menu_items(self):
        return {}