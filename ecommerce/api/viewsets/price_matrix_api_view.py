from ecommerce.api.serializers.price_matrix_serializer import PriceMatrixSerializer
from ecommerce.models.sales.price_matrix import PriceMatrix
from generics.api.views.generic_api_view import GenericAPIView


class PriceMatrixAPIView(GenericAPIView):
    queryset = PriceMatrix.objects.all()
    serializer_class = PriceMatrixSerializer

    def filter_criteria(self, request, queryset):

        return queryset
