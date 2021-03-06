from django.conf.urls import url

from book_rental.views.book_details import BookDetailsView
from book_rental.views.book_search_view import BookSearchView
from book_rental.views.browse_view import BookBrowseView

urlpatterns = [
    url(r'^browse/$', BookBrowseView.as_view(), name="book_browse_view"),
    # url(r'^browse/(?P<slug>[-\w]+)/$', BookBrowseView.as_view(), name="book_browse_view"),
    url(r'^browse/(?P<slug>.+)/$', BookBrowseView.as_view(), name="book_browse_view"),
    url(r'^search/$', BookSearchView.as_view(), name="book_search_view"),
    url(r'^details/$', BookDetailsView.as_view(), name="book_details_view"),
]
