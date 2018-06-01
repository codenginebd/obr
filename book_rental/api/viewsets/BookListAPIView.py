from decimal import Decimal
import copy
from django.db.models.query_utils import Q
from book_rental.api.serializers.book_list_serializer import BookSerializer
from book_rental.models.sales.book import Book
from generics.api.views.generic_api_view import GenericAPIView
from inventory.models.inventory import Inventory


class BookListAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def filter_criteria(self, request, queryset):
        out_of_stock = request.GET.get("out-of-stock")
        isbn = request.GET.get("isbn")
        keyword = request.GET.get('keyword')
        language = request.GET.get("lang")
        rating = request.GET.get("rating")
        use_status = request.GET.get("use-status")
        print_type = request.GET.get("print-type")
        category = request.GET.get("cat")
        author = request.GET.get("author")
        publisher = request.GET.get("publisher")

        inventory_objects = Inventory.objects.filter(product_model=Book.__name__)

        inventory_used = False

        if isbn:
            if len(isbn) == 10:
                queryset = queryset.filter(Q(isbn__isnull=False) & Q(isbn=isbn))
            elif len(isbn) == 13:
                queryset = queryset.filter(Q(isbn13__isnull=False) & Q(isbn13=isbn))
            else:
                queryset = queryset.model.objects.none()

        if keyword:
            queryset = queryset.filter(tags__name__icontains=keyword)

        if language:
            language_list = language.split(",")
            if language_list:
                OR_FILTER = Q(language__short_name=language_list[0])
                for i, lang in enumerate(language_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(language__short_name=lang)
            queryset = queryset.filter(OR_FILTER)

        if rating:
            rating_list = rating.split(",")
            try:
                rating_list = [Decimal(r) for r in rating_list]
            except:
                rating_list = []

            if rating_list:
                rating_min = min(rating_list) - Decimal(0.5)
                rating_max = max(rating_list) + Decimal(0.5)
                queryset = queryset.filter(rating__gte=rating_min, rating__lte=rating_max)
            else:
                queryset = queryset.model.objects.none()

        if use_status:
            us_list = []
            use_status_list = use_status.split(",")
            if use_status_list:
                OR_FILTER = Q(is_new=use_status_list[0])
                for i, us in enumerate(use_status_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(is_new=us)
            if us_list:
                inventory_objects = inventory_objects.filter(OR_FILTER)
                inventory_used = True

        if print_type:
            print_type_list = print_type.split(",")
            if print_type_list:
                OR_FILTER = Q(print_type=print_type_list[0])
                for i, pt in enumerate(print_type_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(print_type=pt)
                inventory_objects = inventory_objects.filter(OR_FILTER)
                inventory_used = True

        if out_of_stock:
            # Get all products from the queryset which has stock in inventory only.
            inventory_objects = inventory_objects.filter(stock__gt=0)

            inventory_used = True

        if category:
            category_list = category.split(",")
            if category_list:
                OR_FILTER = Q(categories__slug=category_list[0])
                for i, cat in enumerate(category_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(categories__slug=cat)
                queryset = queryset.filter(OR_FILTER)

        if author:
            author_list = author.split(",")
            if author_list:
                OR_FILTER = Q(authors__slug=author_list[0])
                for i, a in enumerate(author_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(authors__slug=a)
                queryset = queryset.filter(OR_FILTER)

        if publisher:
            publisher_list = publisher.split(",")
            if publisher_list:
                OR_FILTER = Q(publisher__slug=publisher_list[0])
                for i, pub in enumerate(publisher_list):
                    if i == 0:
                        continue
                    else:
                        OR_FILTER |= Q(publisher__slug=pub)
                queryset = queryset.filter(OR_FILTER)

        if inventory_used:
            product_ids = queryset.values_list('pk', flat=True)
            inventory_objects = inventory_objects.filter(product_id__in=product_ids)
            inventory_product_ids = inventory_objects.values_list('product_id', flat=True)
            queryset = queryset.filter(pk__in=inventory_product_ids)

        return queryset

    def filter_criteria1(self, request, queryset):
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
                
        inventory_filter = False
                
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__)
                
        is_rent_available = request.GET.get('rent-available')
        if is_rent_available:
            try:
                is_rent_available = int(is_rent_available)
                is_rent_available = True if is_rent_available else False
                inventory_objects = inventory_objects.filter(available_for_rent=is_rent_available)
                inventory_filter = True
            except Exception as exp:
                pass
                
        used_type = request.GET.get('used')
        if used_type:
            try:
                used_type = int(used_type)
                is_new = 0 if used_type else 1
                inventory_objects = inventory_objects.filter(is_new=is_new)
                inventory_filter = True
            except Exception as exp:
                pass
                
        printing_type = request.GET.get('print') # COL, ORI, ECO
        if printing_type:
            printing_type = printing_type.upper()
            inventory_objects = inventory_objects.filter(print_type=printing_type)
            inventory_filter = True
            
        if inventory_filter:
            inventory_book_ids = inventory_objects.values_list('product_id', flat=True).distinct()
            queryset = queryset.filter(pk__in=inventory_book_ids)

        queryset = queryset.values_list('pk', flat=True).distinct()

        queryset = queryset.model.objects.filter(pk__in=queryset)

        return queryset
