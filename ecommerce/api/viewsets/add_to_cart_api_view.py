from generics.api.views.br_api_view import BRAPIView

"""
Cart Structure

{
    'last_modified': datetime,
    'items': 
    {
        1213: 
        {
            'buy_items': 
            [
                {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'promo_code': 'ZacdaSds',
                    'promo_amount': 200,
                    'discount_applied': True,
                    'discount_offer_type': 'amount',
                    'discount_amount': 300,
                    'total': 500,
                    'currency_code': 'BDT'
                }
            ],
            'rent_items': 
            [
                {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'rent_days': 30,
                    'promo_code': 'ZacdaSds',
                    'promo_amount': 200,
                    'discount_applied': True,
                    'discount_offer_type': 'amount',
                    'discount_amount': 300,
                    'total': 500,
                    'currency_code': 'BDT'
                }
            ]
        } 
    }
}

"""

class AddToCartAPIView(BRAPIView):

    def handle_buy_to_cart(self, product_type, product_code, is_new, print_type, **kwargs):
        pass
        
    def handle_rent_to_cart(self, product_type, product_code, is_new, print_type, rent_days, **kwargs):
        pass 

    def handle_post(self, request):
        product_type = request.query_params.get('product_type') # Book
        product_id = request.query_params.get('product_id')
        is_new = request.query_params.get('is_new', 0) # 1/0
        print_type = request.query_params.get('print_type') # ORI/COL/ECO
        buy_type = request.query_params.get('buy_type') # buy/rent
        qty = request.query_params.get('qty')
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