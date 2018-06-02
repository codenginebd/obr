from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer


class GenericAPIView(ListAPIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = ()
    http_method_names = ['get']
    permission_classes = ()
    paginate_by = 10

    def filter_criteria(self, request, queryset):
        return queryset

    def get_queryset(self):
        queryset = super(GenericAPIView, self).get_queryset()
        return self.filter_criteria(self.request, queryset)

    def get_context_data(self, **kwargs):
        context = super(GenericAPIView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["total"] = queryset.count()
        context["results"] = queryset
        return context