from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from book_rental.api.serializers.author_serializer import AuthorSerializer
from book_rental.models.author import Author
from generics.api.views.generic_api_view import GenericAPIView


class AuthorAPIView(GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    renderer_classes = ( JSONRenderer, )
    http_method_names = ['get']

    def get(self, request, format=None):
        queryset = Author.objects.all()
        category_id = request.GET.get('cid')
        if category_id:
            try:
                category_id = int(category_id)
                #queryset = queryset.filter(parent_id=parent_id)
            except Exception as exp:
                pass
        serializer_instance = AuthorSerializer(queryset, many=True)
        return Response(serializer_instance.data)
