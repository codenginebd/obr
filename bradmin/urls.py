from django.conf.urls import url, include

from bradmin.views.admin_logs_view import AdminLogView
from bradmin.views.books_views import AdminBooksView, AdminBooksUploadView
from bradmin.views.admin_error_log_view import AdminErrorLogView, AdminErrorLogsDetailsView
from bradmin.views.category_views import AdminCategoryView, AdminCategoryUploadView, AdminCategoryListView, \
    AdminCategoryDownloadView, AdminCategoryActivateView, AdminCategoryDeactivateView, AdminCategoryDeleteView, \
    AdminCategoryDetailsView, AdminCategoryCreateView, AdminCategoryUpdateView
from bradmin.views.publisher_views import AdminPublisherListView, AdminBookPublisherUploadView, \
    AdminBookPublisherDownloadView, AdminBookPublisherActivateView, AdminBookPublisherDeactivateView, \
    AdminBookPublisherDeleteView, AdminBookPublisherDetailsView
from bradmin.views.views import AdminHomeView, AdminLoginView, AdminLogoutView

urlpatterns = [
    url(r'^$', AdminHomeView.as_view(), name='admin_home_view'),
    url(r'^login/', AdminLoginView.as_view(), name="admin_login_view"),
    url(r'^logout/', AdminLogoutView.as_view(), name="admin_logout_view"),
    #Category
    url(r'^category/', AdminCategoryListView.as_view(), name="admin_category_view"),
    url(r'^category-upload/', AdminCategoryUploadView.as_view(), name="admin_category_upload_view"),
    url(r'^category-download/', AdminCategoryDownloadView.as_view(), name="admin_category_download_view"),
    url(r'^category-activate/', AdminCategoryActivateView.as_view(), name="admin_category_activate_view"),
    url(r'^category-deactivate/', AdminCategoryDeactivateView.as_view(), name="admin_category_deactivate_view"),
    url(r'^category-delete/', AdminCategoryDeleteView.as_view(), name="admin_category_delete_view"),
    url(r'^category-details/(?P<pk>[0-9]+)/$', AdminCategoryDetailsView.as_view(), name="admin_category_details_view"),
    url(r'^category-create/$', AdminCategoryCreateView.as_view(), name="admin_category_create_view"),
    url(r'^category-edit/(?P<pk>[0-9]+)/$', AdminCategoryUpdateView.as_view(), name="admin_category_edit_link_view"),
    #Publisher
    url(r'^publishers/', AdminPublisherListView.as_view(), name="admin_publishers_view"),
    url(r'^publishers-upload/', AdminBookPublisherUploadView.as_view(), name="admin_book_publisher_upload_view"),
    url(r'^publishers-download/', AdminBookPublisherDownloadView.as_view(), name="admin_book_publisher_download_view"),
    url(r'^publishers-activate/', AdminBookPublisherActivateView.as_view(), name="admin_book_publisher_activate_view"),
    url(r'^publishers-deactivate/', AdminBookPublisherDeactivateView.as_view(), name="admin_book_publisher_deactivate_view"),
    url(r'^publishers-delete/', AdminBookPublisherDeleteView.as_view(), name="admin_book_publisher_delete_view"),
    url(r'^publishers-details/(?P<pk>[0-9]+)/$', AdminBookPublisherDetailsView.as_view(), name="admin_book_publisher_details_view"),
    url(r'^publishers-create/$', AdminCategoryCreateView.as_view(), name="admin_book_publisher_create_view"),
    url(r'^publishers-edit/(?P<pk>[0-9]+)/$', AdminCategoryUpdateView.as_view(), name="admin_book_publisher_edit_link_view"),
    #Books
    url(r'^books/', AdminBooksView.as_view(), name="admin_books_view"),
    url(r'^books-upload/', AdminBooksUploadView.as_view(), name="admin_books_upload_view"),

    url(r'^error-logs/', AdminErrorLogView.as_view(), name="admin_error_logs_view"),
    url(r'^error-log/details/(?P<pk>[0-9]+)/$', AdminErrorLogsDetailsView.as_view(), name="admin_error_log_details_view"),
]
