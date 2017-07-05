from rest_framework.response import Response

from book.api.serializers.book_list_serializer import BookListSerializer
from book.models.book import Book
from generics.api.views.generic_api_view import GenericAPIView


class BookListAPIView(GenericAPIView):
    model = Book
    serializer_class = BookListSerializer

    def get(self, request, format=None):
        serializer_instance = BookListSerializer(Book.objects.all(), many=True)
        return Response(serializer_instance.data)
