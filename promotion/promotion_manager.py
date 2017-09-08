

class PromotionManager(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def apply_promotion(self, cart):  # return is_promotion_applied, promotion_code
        self.cart = cart
        return False, None
        