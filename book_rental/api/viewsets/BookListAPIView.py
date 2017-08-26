from django.db.models.query_utils import Q

from book_rental.api.serializers.book_list_serializer import BookSerializer
from book_rental.models.sales.book import Book
from generics.api.views.generic_api_view import GenericAPIView


class BookListAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def filter_criteria(self, request, queryset):
        keyword = request.GET.get('q')
        queryset = queryset.filter(Q(isbn__iexact=keyword) | Q(title__icontains=keyword) | Q(title_2__icontains=keyword)
                                       | Q(authors__name__icontains=keyword) | Q(authors__name_2__icontains=keyword)
                                       | Q(publisher__name=keyword) | Q(publisher__name_2__icontains=keyword)
                                       | Q(tags__name__icontains=keyword)).values('pk')
        queryset = queryset.model.objects.filter(pk__in=queryset)
        return queryset
