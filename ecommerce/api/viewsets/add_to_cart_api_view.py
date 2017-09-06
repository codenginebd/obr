from generics.api.views.br_api_view import BRAPIView

class AddToCartAPIView(BRAPIView):

    def handle_post(self, request):
        product_type = request.query_params.get('ptype')
        product_code = request.query_params.get('pcode')
        used = request.query_params.get('used', 0)
        is_new = True if not used else False
        print_type = request.query_params.get('pr-type')
        buy_type = request.query_params.get('buy-type') # buy or rent
        if buy_type == 'rent':
            rent_days = request.query_params.get('days')
            try:
                rent_days = int(rent_days)
                
            except Exception as exp:
                pass
        
    def create_post_response(self, request, data, *args, **kwargs):
        return {}