from django.conf.urls import url, include

from bradmin.views.books_views import AdminBooksView, AdminBooksUploadView
from bradmin.views.category_views import AdminCategoryView, AdminCategoryUploadView, AdminCategoryListView
from bradmin.views.views import AdminHomeView, AdminLoginView, AdminLogoutView

urlpatterns = [
    url(r'^$', AdminHomeView.as_view(), name='admin_home_view'),
    url(r'^login/', AdminLoginView.as_view(), name="admin_login_view"),
    url(r'^logout/', AdminLogoutView.as_view(), name="admin_logout_view"),
    url(r'^category/', AdminCategoryListView.as_view(), name="admin_category_view"),
    url(r'^category-upload/', AdminCategoryUploadView.as_view(), name="admin_category_upload_view"),

    #Books
    url(r'^books/', AdminBooksView.as_view(), name="admin_books_view"),
    url(r'^books-upload/', AdminBooksUploadView.as_view(), name="admin_books_upload_view"),
]
