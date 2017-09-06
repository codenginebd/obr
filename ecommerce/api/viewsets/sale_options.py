from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ecommerce.models.sales.price_matrix import PriceMatrix
from generics.api.views.br_api_view import BRAPIView


class SaleOptionsAPIView(BRAPIView):

    def get_queryset(self, **kwargs):
        return PriceMatrix.objects.all()
        
    def filter_criteria(self, request, queryset):
        product_type = request.GET.get('ptype')
        product_code = request.GET.get('pcode')
        queryset = queryset.filter(product_model=product_type,product_code=product_code)
        return queryset
        
    def get_many(self):
        return False
        
    def create_response(self, request, queryset):
        response = {}
        for q_object in queryset:
            if q_object.is_new:
                if not 'New' in response.keys():
                    response['New'] = [ q_object.print_type  ]
                else:
                    response['New'] += [ q_object.print_type  ]
            else:
                if not 'Used' in response.keys():
                    response['Used'] = [ q_object.print_type  ]
                else:
                    response['Used'] += [ q_object.print_type  ]
        return response