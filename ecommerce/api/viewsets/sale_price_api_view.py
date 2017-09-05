from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from generics.api.views.br_api_view import BRAPIView


class SalePriceAPIView(BRAPIView):

    def get_queryset(self, **kwargs):
        return PriceMatrix.objects.all()
        
    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        print_type  = request.GET.get('pr-type', 'ECO')
        is_used = request.GET.get('used', 0)
        is_new = True if not is_used else False
        queryset = queryset.filter(product_model=product_type,product_code=product_code,print_type=print_type,is_new=is_new)
        return queryset
        
    def create_response(self, request, queryset):
        response = {}
        if queryset.exists():
            q_object = queryset.first()
            response['product_type'] = q_object.product_model 
            response['product_code'] = q_object.product_code 
            response['product_id'] = q_object.pk
            response['is_new'] = q_object.is_new
            response['print_type'] = q_object.print_type
            response['base_price'] = q_object.base_price
            response['market_price'] = q_object.market_price
            response['currency_code'] = q_object.currency.short_name
            response['special_price'] = q_object.special_price
            response['o_price_p'] = q_object.offer_price_p
            response['o_price_v'] = q_object.offer_price_v
            response['offer_date_start'] = q_object.offer_date_start
            response['offer_date_end'] = q_object.offer_date_end
        return response