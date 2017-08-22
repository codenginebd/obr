from ecommerce.api.serializers.rent_plan_serializer import RentPlanSerializer
from ecommerce.models.rent_plan import RentPlan
from generics.api.views.generic_api_view import GenericAPIView


class RentPlanAPIView(GenericAPIView):
    queryset = RentPlan.objects.all()
    serializer_class = RentPlanSerializer
