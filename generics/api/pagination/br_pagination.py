from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from generics.api.mixins.pagination_mixin import BRPaginationMixin


class BRPagination(PageNumberPagination, BRPaginationMixin):

    def __init__(self, request, queryset, page_size=20, *args, **kwargs):
        self.request = request
        self.make_pagination(request=request, queryset=queryset, page_size=page_size, *args, **kwargs)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })