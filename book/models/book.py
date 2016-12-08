from django.db import models
from book.models.category import BookCategory
from generics.models.base_entity import BaseEntity


class Book(BaseEntity):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    category = models.ForeignKey(BookCategory, null=True)

    @classmethod
    def apply_search(cls, queryset, request=None, **kwargs):
        if request and request.GET.get('id'):
            search_criteria = int(request.GET.get('id'))
            queryset = queryset.filter(pk=search_criteria)
        return queryset