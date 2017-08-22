from book_rental.api.serializers.book_list_serializer import BookSerializer
from book_rental.models.sales.book import Book
from generics.api.views.generic_api_view import GenericAPIView


class BookListAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def filter_criteria(self, request, queryset):

        return queryset
