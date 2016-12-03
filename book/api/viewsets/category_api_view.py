from rest_framework.response import Response
from book.api.serializers.category_serializer import BookCategorySerializer
from book.models.category import BookCategory
from generics.api.views.generic_api_view import GenericAPIView


class BookCategoryAPIView(GenericAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['get']

    def get(self, request, format=None):
        serializer_instance = BookCategorySerializer(BookCategory.objects.all(), many=True)
        return Response(serializer_instance.data)
