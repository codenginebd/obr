"""book_rental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from bauth.api.views.api_login_view import APILoginView
from book_rental.api.viewsets.BookListAPIView import BookListAPIView
from book_rental.api.viewsets.author_api_view import AuthorAPIView, AuthorAPIViewNoPagination
from book_rental.api.viewsets.publisher_api_view import PublisherAPIView, PublisherAPIViewNoPagination
from book_rental.views.browse_view import BookBrowseView
from book_rental.views.profile_view import ProfileView
from cart_view import BasketView
from ecommerce.api.viewsets.category_api_view import CategoryAPIView, CategoryAPIViewNoPagination
from ecommerce.api.viewsets.price_matrix_api_view import PriceMatrixAPIView
from ecommerce.api.viewsets.rent_plan_api_view import RentPlanAPIView
from ecommerce.api.viewsets.sale_price_api_view import SalePriceAPIView
from home_view import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^admin/', include('bradmin.urls')),
    url(r'^auth/', include('bauth.urls')),
    url(r'^books/', include('book_rental.urls')),
    url(r'^my-cart/', BasketView.as_view(), name='my_cart_view'),
    url(r'^profile/(?P<username>.+)', ProfileView.as_view(), name='profile_view'),
]

# Include api's
urlpatterns += [
    # url(r'^api/v1/$', book_router.get_api_root_view(), name=book_router.root_view_name),
]

urlpatterns += [
    url('^api/v1/category-browse/$', CategoryAPIView.as_view()),
    url('^api/v1/author-browse/$', AuthorAPIView.as_view()),
    url('^api/v1/publisher-browse/$', PublisherAPIView.as_view()),
    url('^api/v1/categories/$', CategoryAPIViewNoPagination.as_view()),
    url('^api/v1/authors/$', AuthorAPIViewNoPagination.as_view()),
    url('^api/v1/publishers/$', PublisherAPIViewNoPagination.as_view()),
    url('^api/v1/books/$', BookListAPIView.as_view()),
    url('^api/v1/rent-plans/$', RentPlanAPIView.as_view()),
    url('^api/v1/sale-price/$', SalePriceAPIView.as_view()),
    url('^api/v1/product-prices/$', PriceMatrixAPIView.as_view()),
    url('^api/v1/login/$', APILoginView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
