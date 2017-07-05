class FilterModelMixin(object):

    @classmethod
    def apply_filter(cls, queryset, request=None, **kwargs):
        return queryset