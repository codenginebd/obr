from ecommerce.api.serializers.rent_plan_serializers import RentPlanRelationSerializer
from ecommerce.models.sales.price_matrix import PriceMatrix
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.api.serializers.base_model_serializer import BaseModelSerializer
from rest_framework import serializers


class PriceMatrixSerializer(BaseModelSerializer):
    currency_code = serializers.SerializerMethodField()
    rent_plans = serializers.SerializerMethodField()

    def get_currency_code(self, obj):
        return obj.currency.short_name

    def get_rent_plans(self, obj):
        rent_plan_rel_objects = RentPlanRelation.objects.filter(price_matrix_id=obj.pk)
        return RentPlanRelationSerializer(rent_plan_rel_objects, many=True).data

    class Meta:
        model = PriceMatrix
        fields = ('id', 'code', 'product_code', 'product_model', 'market_price',
                  'base_price', 'currency_code', 'rent_plans', 'is_new', 'print_type', 'special_price',
                  'offer_date_start', 'offer_date_end', 'offer_price_p', 'offer_price_v')
