from django.db.models.query_utils import Q

from book_rental.api.serializers.publisher_serializer import PublisherSerializer
from book_rental.models.book_publisher import BookPublisher
from generics.api.views.generic_api_view import GenericAPIView


class PublisherAPIView(GenericAPIView):
    queryset = BookPublisher.objects.all()
    serializer_class = PublisherSerializer

    def filter_criteria(self, request, queryset):
        category_id = request.GET.get('cid')
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(Q(book__publisher__isnull=False) & Q(book__publisher__id=category_id))
            except Exception as exp:
                queryset = queryset.model.objects.none()
        ids = list(set(queryset.values_list('pk', flat=True)))
        return queryset.model.objects.filter(pk__in=ids)


class PublisherAPIViewNoPagination(PublisherAPIView):
    pagination_class = None
