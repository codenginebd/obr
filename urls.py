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
from book_rental.views.author_views import AuthorBrowseView, AuthorFilterListView
from book_rental.views.profile_view import ProfileView
from book_rental.views.publisher_views import PublisherBrowseView
from cart_view import BasketView
from ecommerce.api.viewsets.category_api_view import CategoryAPIView, CategoryAPIViewNoPagination
from ecommerce.api.viewsets.price_matrix_api_view import PriceMatrixAPIView
from ecommerce.api.viewsets.rent_plan_api_view import RentPlanAPIView
from ecommerce.api.viewsets.rent_plan_options import RentPlanOptionsAPIView
from ecommerce.api.viewsets.sale_options import SaleOptionsAPIView
from ecommerce.api.viewsets.sale_price_api_view import SalePriceAPIView
from home_view import HomeView
from ecommerce.api.viewsets.add_to_cart_api_view import AddToCartAPIView
# Books Import
from book_rental.views.book_details import BookDetailsView
from book_rental.views.book_search_view import BookSearchView
from book_rental.views.browse_view import BookBrowseView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^admin/', include('bradmin.urls')),
    url(r'^auth/', include('bauth.urls')),
    url(r'^shopping/', include('ecommerce.urls')),
    url(r'^my-cart/', BasketView.as_view(), name='my_cart_view'),
    url(r'^profile/(?P<username>.+)', ProfileView.as_view(), name='profile_view'),

    # Books
    url(r'^books/browse/$', BookBrowseView.as_view(), name="book_browse_view"),
    url(r'^books/browse/(?P<slug>.+)/$', BookBrowseView.as_view(), name="book_browse_view"),
    url(r'^books/search/$', BookSearchView.as_view(), name="book_search_view"),
    url(r'^books/details/$', BookDetailsView.as_view(), name="book_details_view"),

    #Authors
    url(r'^authors/browse/$', AuthorBrowseView.as_view(), name="author_browse_view"),
    url(r'^author/(?P<pk>[0-9]+)/$', AuthorFilterListView.as_view(), name="author_browse_filter_view"),

    #Publishers
    url(r'^publishers/browse/$', PublisherBrowseView.as_view(), name="publisher_browse_view"),

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
    url('^api/v1/sale-options/$', SaleOptionsAPIView.as_view()),
    url('^api/v1/rent-plans/$', RentPlanAPIView.as_view()),
    url('^api/v1/rent-plan-options/$', RentPlanOptionsAPIView.as_view()),
    url('^api/v1/shopping/add-to-cart/$', AddToCartAPIView.as_view()),
    url('^api/v1/sale-price/$', SalePriceAPIView.as_view()),
    url('^api/v1/product-productprices/$', PriceMatrixAPIView.as_view()),
    url('^api/v1/login/$', APILoginView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
