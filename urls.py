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

from bauth.api.views.api_login_view import APILoginView
from book_rental.api.router import book_router
from book_rental.api.viewsets.BookListAPIView import BookListAPIView
from book_rental.api.viewsets.category_api_view import BookCategoryAPIView
from book_rental.views.browse_view import BookBrowseView
from cart_view import BasketView

from home_view import HomeView

urlpatterns = [
    url(r'^$', BookBrowseView.as_view(), name='home_view'),
    url(r'^admin/', include('bradmin.urls')),
    url(r'^auth/', include('bauth.urls')),
    url(r'^books/', include('book_rental.urls')),
    url(r'^my-basket/', BasketView.as_view(), name='my_basket_view'),
]

# Include API's
urlpatterns += [
    # url(r'^api/v1/$', book_router.get_api_root_view(), name=book_router.root_view_name),
]

urlpatterns += [
    url('^api/v1/category-list/$', BookCategoryAPIView.as_view()),
    url('^api/v1/book_rental-list/$', BookListAPIView.as_view()),
    url('^api/v1/login/$', APILoginView.as_view())
]

urlpatterns += book_router.urls
