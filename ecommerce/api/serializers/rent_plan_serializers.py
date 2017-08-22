from ecommerce.api.serializers.rent_plan_serializer import RentPlanSerializer
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class RentPlanRelationSerializer(BaseModelSerializer):
    plan = RentPlanSerializer()

    class Meta:
        model = RentPlanRelation
        fields = ('id', 'code', 'plan', 'start_time', 'end_time',
                  'is_special_offer', 'special_rate', 'rent_rate')
