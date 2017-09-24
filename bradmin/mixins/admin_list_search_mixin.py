class AdminListSearchMixin(object):
    def get_search_by_options(self):
        return self.model.get_search_by_options()

    def get_advanced_search_options(self):
        return self.model.get_advanced_search_options()

    def apply_search_filter(self, request, queryset):
        return self.model.apply_search_filters(request=request, queryset=queryset)

    def collect_search_by(self, request):
        return request.GET.get('by', None)

    def collect_search_keyword(self, request):
        return request.GET.get('keyword', None)

    def collect_search_advanced_params(self, request):
        params = {}
        for key, value in request.GET.items():
            if key != 'by' and key != 'keyword':
                params[key] = value
        return params