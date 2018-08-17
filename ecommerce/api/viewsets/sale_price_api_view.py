from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from engine.clock.Clock import Clock
from ecommerce.models.sales.price_matrix import PriceMatrix
from generics.api.views.br_api_view import BRAPIView


# http://127.0.0.1:8003/api/v1/sale-price/?ptype=Book&pcode=B-000001&pr-type=ORI&used=true


class SalePriceAPIView(BRAPIView):

    def get_queryset(self, **kwargs):
        return PriceMatrix.objects.all()
        
    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        print_type  = request.GET.get('pr-type', 'ECO')
        is_used = request.GET.get('used', 0)
        is_new = 1 if not is_used or is_used == '0' or is_used == 'false' else 0
        queryset = queryset.filter(product_model=product_type,product_code=product_code,print_type=print_type,is_new=is_new)
        return queryset
        
    def create_response(self, request, queryset):
        response = {}
        if queryset.exists():
        
            utc_ts_now = Clock.utc_timestamp()
        
            q_object = queryset.first()
            
            is_special_offer = False
            if q_object.special_price:
                if q_object.offer_date_start <= utc_ts_now and q_object.offer_date_end >= utc_ts_now:
                    is_special_offer = True
                else:
                    is_special_offer = False
            else:
                is_special_offer = False
            
            response['product_type'] = q_object.product_model 
            response['product_code'] = q_object.product_code 
            response['product_id'] = q_object.pk
            response['is_new'] = q_object.is_new
            response['print_type'] = q_object.print_type
            response['base_price'] = q_object.base_price
            response['market_price'] = q_object.market_price
            response['currency_code'] = q_object.currency.short_name
            if is_special_offer:
                response['special_price'] = True
                response['o_price_p'] = q_object.offer_price_p
                response['o_price_v'] = (q_object.offer_price_p/100) * q_object.base_price
                response['offer_date_start'] = q_object.offer_date_start
                response['offer_date_end'] = q_object.offer_date_end
            else:
                response['special_price'] = False
                response['o_price_p'] = 0
                response['o_price_v'] = 0
                response['offer_date_start'] = 0
                response['offer_date_end'] = 0
            response["sale_price"] = q_object.get_product_sale_price
            
            promotion_text = ""
            if is_special_offer:
                promotion_text = "%.1f" % (100 - q_object.offer_price_p) + "% Less"
            
            response["promotion_text"] = promotion_text
            
        return response