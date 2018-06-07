from django.conf.urls import url
from ecommerce.api.viewsets.add_to_cart_api_view import AddToCartView

urlpatterns = [
    url(r'^add-to-cart/$', AddToCartView.as_view(), name="shopping_add_to_cart_view"),
]