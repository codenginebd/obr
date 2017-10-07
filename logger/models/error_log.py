from django.db import models
from django.urls.base import reverse

from generics.models.base_entity import BaseEntity


class ErrorLog(BaseEntity):
    context = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=500)
    stacktrace = models.TextField(blank=True, null=True)

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_error_log_details_view", kwargs={"pk": object_id})

    @classmethod
    def apply_search_filters(cls, request, queryset):
        context = request.GET.get("context", None)
        by = request.GET.get("by", None)
        keyword = request.GET.get("keyword", None)
        if context:
            queryset = queryset.filter(context=context)
        if by and keyword:
            if by == "id":
                try:
                    keyword = int(keyword)
                    queryset = queryset.filter(pk=keyword)
                except:
                    pass
            elif by == "code":
                queryset = queryset.filter(code=keyword)
        return queryset
    
    @classmethod
    def log(cls, url, stacktrace=None, context=None):
        instance = cls()
        if context:
            instance.context = context
        instance.url = url
        if stacktrace:
            instance.stacktrace = stacktrace
        instance.save()
