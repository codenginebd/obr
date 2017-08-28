from decimal import Decimal
from django.db.models.query_utils import Q
from book_rental.api.serializers.book_list_serializer import BookSerializer
from book_rental.models.sales.book import Book
from generics.api.views.generic_api_view import GenericAPIView


class BookListAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def filter_criteria(self, request, queryset):
        keyword = request.GET.get('q')
        if keyword:
            queryset = queryset.filter(Q(isbn__iexact=keyword) | Q(title__icontains=keyword) | Q(title_2__icontains=keyword)
                                           | Q(authors__name__icontains=keyword) | Q(authors__name_2__icontains=keyword)
                                           | Q(publisher__name__icontains=keyword) | Q(publisher__name_2__icontains=keyword)
                                           | Q(tags__name__icontains=keyword))

        isbn = request.GET.get('isbn')
        if isbn:
            queryset = queryset.filter(isbn__iexact=isbn)

        keyword = request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(tags__name__icontains=keyword)

        book_language = request.GET.get('clang')
        if book_language:
            queryset = queryset.filter(language__short_name__iexact=book_language)

        rating = request.GET.get('rating')
        if rating and rating != 'any':
            try:
                rating = Decimal(rating)
                rating_min = rating - Decimal(0.5)
                rating_max = rating + Decimal(0.5)
                queryset = queryset.filter(rating__gte=rating_min, rating__lte=rating_max)
            except:
                pass

        category_ids = request.GET.get('category')
        if category_ids:
            try:
                category_ids = category_ids.split(',')
                category_ids = [ int(cat_id) for cat_id in category_ids if cat_id ]
                queryset = queryset.filter(categories__id__in=category_ids)
            except Exception as exp:
                pass
                
        author_ids = request.GET.get('author')
        if author_ids:
            try:
                author_ids = author_ids.split(',')
                author_ids = [ int(author_id) for author_id in author_ids if author_id ]
                queryset = queryset.filter(authors__id__in=author_ids)
            except Exception as exp:
                pass
                
        publisher_ids = request.GET.get('publisher')
        if publisher_ids:
            try:
                publisher_ids = publisher_ids.split(',')
                publisher_ids = [ int(publisher_id) for publisher_id in publisher_ids if publisher_id ]
                queryset = queryset.filter(publisher__id__in=publisher_ids)
            except Exception as exp:
                pass

        queryset = queryset.values_list('pk', flat=True).distinct()

        queryset = queryset.model.objects.filter(pk__in=queryset)

        return queryset
