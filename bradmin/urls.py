from django.conf.urls import url, include

from bradmin.views.admin_logs_view import AdminLogView
from bradmin.views.books_views import AdminBooksView, AdminBooksUploadView
from bradmin.views.category_log_view import AdminCategoryLogView
from bradmin.views.category_views import AdminCategoryView, AdminCategoryUploadView, AdminCategoryListView, \
    AdminCategoryDownloadView, AdminCategoryActivateView, AdminCategoryDeactivateView, AdminCategoryDeleteView, \
    AdminCategoryDetailsView
from bradmin.views.views import AdminHomeView, AdminLoginView, AdminLogoutView

urlpatterns = [
    url(r'^$', AdminHomeView.as_view(), name='admin_home_view'),
    url(r'^login/', AdminLoginView.as_view(), name="admin_login_view"),
    url(r'^logout/', AdminLogoutView.as_view(), name="admin_logout_view"),
    url(r'^category/', AdminCategoryListView.as_view(), name="admin_category_view"),
    url(r'^category-upload/', AdminCategoryUploadView.as_view(), name="admin_category_upload_view"),
    url(r'^category-download/', AdminCategoryDownloadView.as_view(), name="admin_category_download_view"),
    url(r'^category-activate/', AdminCategoryActivateView.as_view(), name="admin_category_activate_view"),
    url(r'^category-deactivate/', AdminCategoryDeactivateView.as_view(), name="admin_category_deactivate_view"),
    url(r'^category-delete/', AdminCategoryDeleteView.as_view(), name="admin_category_delete_view"),
    url(r'^category-details/(?P<pk>[0-9]+)/$', AdminCategoryDetailsView.as_view(), name="admin_category_details_view"),

    #Books
    url(r'^books/', AdminBooksView.as_view(), name="admin_books_view"),
    url(r'^books-upload/', AdminBooksUploadView.as_view(), name="admin_books_upload_view"),

    url(r'^category-logs/', AdminCategoryLogView.as_view(), name="admin_category_logs_view"),
]
