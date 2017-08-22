from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer


class GenericAPIView(ListAPIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = ()
    http_method_names = ['get']
    permission_classes = ()

    def filter_criteria(self, request, queryset):
        return queryset

    def get_queryset(self):
        queryset = super(GenericAPIView, self).get_queryset()
        return self.filter_criteria(self.request, queryset)