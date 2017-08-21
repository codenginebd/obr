from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from ecommerce.api.serializers.category_serializer import CategorySerializer
from ecommerce.models.sales.category import ProductCategory
from generics.api.views.generic_api_view import GenericAPIView


class CategoryAPIView(GenericAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = ( JSONRenderer, )
    http_method_names = ['get']

    def get(self, request, format=None):
        queryset = ProductCategory.objects.all()
        parent_id = request.GET.get('pid')
        if parent_id:
            try:
                parent_id = int(parent_id)
                queryset = queryset.filter(parent_id=parent_id)
            except Exception as exp:
                pass
        serializer_instance = CategorySerializer(queryset, many=True)
        return Response(serializer_instance.data)
