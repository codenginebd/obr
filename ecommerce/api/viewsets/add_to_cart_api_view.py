from generics.api.views.br_api_view import BRAPIView

class AddToCartAPIView(BRAPIView):

    def handle_post(self, request):
        pass
        
    def create_post_response(self, request, data, *args, **kwargs):
        return {}