class SearchableModelMixin(object):

    @classmethod
    def apply_search(cls, queryset, request=None, **kwargs):
        return queryset