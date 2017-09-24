class AdminListDataMixin(object):
    def get_table_headers(self):
        return self.model.get_table_headers()

    def prepare_table_data(self, queryset):
        return self.model.prepare_table_data(queryset=queryset)