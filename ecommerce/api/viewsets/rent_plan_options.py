from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from generics.api.views.br_api_view import BRAPIView
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from ecommerce.api.serializers.rent_plan_serializers import RentPlanRelationSerializer


class RentPlanOptionsAPIView(BRAPIView):

    def get_queryset(self, **kwargs):
        return PriceMatrix.objects.all()
        
    def get_many(self):
        return True
        
    def get_serializer_class(self, request, queryset, **kwargs):
        return RentPlanRelationSerializer
        
    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        print_type  = request.GET.get('pr-type', 'ECO')
        is_used = request.GET.get('used', 0)
        is_new = True if not is_used else False
        queryset = queryset.filter(product_model=product_type,product_code=product_code,print_type=print_type,is_new=is_new,is_rent=True)
        if queryset.exists():
            q_object = queryset.first()
            rent_plan_ids = q_object.rent_plans.values_list('pk', flat=True)
            rent_plan_relation_objects = RentPlanRelation.objects.filter(plan_id__in=rent_plan_ids,price_matrix_id=q_object.pk)
            return rent_plan_relation_objects
        return RentPlanRelation.objects.none()