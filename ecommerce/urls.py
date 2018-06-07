from django.conf.urls import url
from ecommerce.api.viewsets.add_to_cart_api_view import AddToCartAPIView

urlpatterns = [
    url(r'^add-to-cart/$', AddToCartAPIView.as_view(), name="shopping_add_to_cart_view"),
]