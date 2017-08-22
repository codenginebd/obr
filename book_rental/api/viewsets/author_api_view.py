from book_rental.api.serializers.author_serializer import AuthorSerializer
from book_rental.models.author import Author
from generics.api.views.generic_api_view import GenericAPIView


class AuthorAPIView(GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def filter_criteria(self, request, queryset):
        category_id = request.GET.get('cid')
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(book__categories__id=category_id)
            except Exception as exp:
                queryset = queryset.model.objects.none()
        return queryset

class AuthorAPIViewNoPagination(AuthorAPIView):
    pagination_class = None
