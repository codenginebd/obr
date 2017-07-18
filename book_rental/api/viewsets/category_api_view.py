from rest_framework.response import Response
from book_rental.api.serializers.category_serializer import BookCategorySerializer
from generics.api.views.generic_api_view import GenericAPIView
from generics.models.sales.category import ProductCategory


class BookCategoryAPIView(GenericAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['get']

    def get(self, request, format=None):
        serializer_instance = BookCategorySerializer(ProductCategory.objects.all(), many=True)
        return Response(serializer_instance.data)
