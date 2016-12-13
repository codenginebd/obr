from django.db import models
from django.db.models.query_utils import Q
from generics.middleware.br_middleware import BRRequestMiddleware


class BaseEntityModelManager(models.Manager):
    _filter = None

    def __init__(self, *args, filter=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._filter = filter
        self.kwargs = kwargs

    def get_queryset(self):
        current_request = BRRequestMiddleware.get_request()

        queryset = super().get_queryset()
        if self._filter:
            queryset = queryset.filter(Q(**self._filter))
        queryset = self.model.apply_permissions(queryset, request=current_request, **(self.kwargs))
        queryset = self.model.apply_filter(queryset, request=current_request, **(self.kwargs))
        queryset = self.model.apply_search(queryset, request=current_request, **(self.kwargs))
        return queryset