

class PromotionManager(object):

    def __init__(self, cart, **kwargs):
        self.cart = cart
        self.kwargs = kwargs
        
    def apply_promotion(self):  # return is_promotion_applied, promotion_code
        pass
        