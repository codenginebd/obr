from django.conf.urls import url

from book.views.book_search_view import BookSearchView
from book.views.browse_view import BookBrowseView

urlpatterns = [
    url(r'^browse/$', BookBrowseView.as_view(), name="book_browse_view"),
    url(r'^search/$', BookSearchView.as_view(), name="book_search_view"),
]
