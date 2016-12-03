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
from book.api.router import book_router
from book.api.viewsets.category_api_view import BookCategoryAPIView

from home_view import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_view'),
    # url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('bauth.urls')),
    url(r'^books/', include('book.urls')),
]

# Include API's
urlpatterns += [
    # url(r'^api/v1/$', book_router.get_api_root_view(), name=book_router.root_view_name),
]

urlpatterns += [
    url('^api/v1/category-list/$', BookCategoryAPIView.as_view())
]


urlpatterns += book_router.urls
