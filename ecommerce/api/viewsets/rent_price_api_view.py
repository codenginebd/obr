from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from ecommerce.models.sales.price_matrix import PriceMatrix
from generics.api.views.br_api_view import BRAPIView


class RentPriceAPIView(BRAPIView):

    def get_queryset(self, **kwargs):
        return RentPlanRelation.objects.all()

    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        print_type = request.GET.get('pr-type', 'ECO')
        is_used = request.GET.get('used', 0)
        is_new = 1 if not is_used or is_used == '0' or is_used == 'false' else 0
        days = request.GET.get('days')
        days = int(days)
        price_matrix_objects = PriceMatrix.objects.filter(product_model=product_type, product_code=product_code, print_type=print_type,
                                   is_new=is_new)
        if price_matrix_objects.exists():
            price_matrix_object = price_matrix_objects.first()
            rent_plans = RentPlan.objects.filter(days=days)
            if rent_plans.exists():
                rent_plan = rent_plans.first()

                return RentPlanRelation.objects.filter(plan_id=rent_plan.pk, price_matrix_id=price_matrix_object.pk)

        return RentPlanRelation.objects.none()

    def create_response(self, request, queryset):
        response = {}
        if queryset.exists():
            q_object = queryset.first()
            response["rent_rate"] = q_object.rent_rate
            response["rent_price"] = q_object.rent_price
            response["special_rent_price"] = q_object.special_rent_price
            response["is_special_offer"] = q_object.is_special_offer
            response["special_rate"] = q_object.special_rate
            response["start_time"] = q_object.start_time
            response["end_time"] = q_object.end_time
        return response