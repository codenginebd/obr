from generics.api.views.br_api_view import BRAPIView

class AddToCartAPIView(BRAPIView):

    def handle_buy_to_cart(self, product_type, product_code, is_new, print_type, **kwargs):
        pass
        
    def handle_rent_to_cart(self, product_type, product_code, is_new, print_type, rent_days, **kwargs):
        pass 

    def handle_post(self, request):
        product_type = request.query_params.get('ptype')
        product_code = request.query_params.get('pcode')
        used = request.query_params.get('used', 0)
        is_new = True if not used else False
        print_type = request.query_params.get('pr-type')
        buy_type = request.query_params.get('buy-type') # buy or rent
        if buy_type == 'rent':
            rent_days = request.query_params.get('days')
            rent_days = int(rent_days)
            self.handle_rent_to_cart(product_type, product_code, is_new, print_type, rent_days)
        else:
            self.handle_buy_to_cart(product_type, product_code, is_new, print_type)
            
                
    def is_valid(self, request):
        product_type = request.query_params.get('ptype')
        product_code = request.query_params.get('pcode')
        used = request.query_params.get('used')
        is_new = True if not used else False
        print_type = request.query_params.get('pr-type')
        buy_type = request.query_params.get('buy-type') # buy or rent
        valid = True
        if any([ not product_type, not product_code, not used, not print_type, not buy_type ]):
            valid = False
        if buy_type == 'rent':
            rent_days = request.query_params.get('days')
            try:
                rent_days = int(rent_days)
            except Exception as exp:
                valid = False
        return valid
        
    def create_post_response(self, request, data, *args, **kwargs):
        return {}