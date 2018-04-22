from ecommerce.api.serializers.rent_plan_serializer import RentPlanSerializer
from ecommerce.models.rent_plan import RentPlan
from generics.api.views.generic_api_view import GenericAPIView
from generics.api.views.br_api_view import BRAPIView
from ecommerce.models.sales.price_matrix import PriceMatrix


class RentPlanAPIView(BRAPIView):
    queryset = RentPlan.objects.all()
    serializer_class = RentPlanSerializer

    def get_queryset(self, **kwargs):
        return RentPlan.objects.all()

    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        print_type = request.GET.get('pr-type', 'ECO')
        is_used = request.GET.get('used', 0)
        is_new = 1 if not is_used or is_used == '0' or is_used == 'false' else 0
        price_matrix_objects = PriceMatrix.objects.filter(product_model=product_type, product_code=product_code, print_type=print_type,
                                   is_new=is_new)
        if price_matrix_objects.exists():
            return price_matrix_objects.first().rent_plans.all()
        return RentPlan.objects.all()

    def create_response(self, request, queryset):
        if queryset.exists():
            return {
                "status": "SUCCESS",
                "items": [self.serializer_class(instance).data for instance in queryset]
            }
        else:
            return {
                "status": "FAILED",
                "items": "NO_DATA"
            }
