from django.conf.urls import url

from bradmin.views.admin_error_log_view import AdminErrorLogView, AdminErrorLogsDetailsView
from bradmin.views.book.book_views import AdminBooksListView, AdminBookUploadView, AdminBookDownloadView, \
    AdminBookActivateView, AdminBookDeactivateView, AdminBookDeleteView
from bradmin.views.books_views import AdminBooksView, AdminBooksUploadView
from bradmin.views.category.category_views import AdminCategoryUploadView, AdminCategoryListView, \
    AdminCategoryDownloadView, AdminCategoryActivateView, AdminCategoryDeactivateView, AdminCategoryDeleteView, \
    AdminCategoryDetailsView, AdminCategoryCreateView, AdminCategoryUpdateView
from bradmin.views.publisher.publisher_views import AdminPublisherListView, AdminBookPublisherUploadView, \
    AdminBookPublisherDownloadView, AdminBookPublisherActivateView, AdminBookPublisherDeactivateView, \
    AdminBookPublisherDeleteView, AdminBookPublisherDetailsView, AdminBookPublisherCreateView, \
    AdminBookPublisherUpdateView
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
    url(r'^publishers-create/$', AdminBookPublisherCreateView.as_view(), name="admin_book_publisher_create_view"),
    url(r'^publishers-edit/(?P<pk>[0-9]+)/$', AdminBookPublisherUpdateView.as_view(), name="admin_book_publisher_edit_link_view"),
    #Books
    url(r'^books/', AdminBooksListView.as_view(), name="admin_book_list_view"),
    url(r'^books-upload/', AdminBookUploadView.as_view(), name="admin_book_upload_view"),
    url(r'^books-download/', AdminBookDownloadView.as_view(), name="admin_book_download_view"),
    url(r'^books-activate/', AdminBookActivateView.as_view(), name="admin_book_activate_view"),
    url(r'^books-deactivate/', AdminBookDeactivateView.as_view(),name="admin_book_deactivate_view"),
    url(r'^publishers-delete/', AdminBookDeleteView.as_view(), name="admin_book_delete_view"),

    url(r'^error-logs/', AdminErrorLogView.as_view(), name="admin_error_logs_view"),
    url(r'^error-log/details/(?P<pk>[0-9]+)/$', AdminErrorLogsDetailsView.as_view(), name="admin_error_log_details_view"),
]
