from ecommerce.models.rent_plan import RentPlan
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class RentPlanSerializer(BaseModelSerializer):

    class Meta:
        model = RentPlan
        fields = ('id', 'code', 'name', 'days')
