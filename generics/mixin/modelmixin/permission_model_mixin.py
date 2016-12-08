class PermissionModelMixin(object):

    @classmethod
    def apply_permissions(cls, queryset, request=None, **kwargs):

        return queryset