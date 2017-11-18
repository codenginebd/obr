from book_rental.mixin.common_data_mixin import CommonDataMixin
from book_rental.models.author import Author
from generics.views.base_filter_list_view import BaseFilterListView
from generics.views.base_list_view import BaseListView


class AuthorBrowseView(BaseListView, CommonDataMixin):
    template_name = "author_browse.html"
    model = Author

    def get_top_menu(self):
        return "author"


class AuthorFilterListView(BaseFilterListView):
    model = Author
    template_name = "author_filter_list_view.html"