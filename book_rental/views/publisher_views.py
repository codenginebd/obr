from book_rental.mixin.common_data_mixin import CommonDataMixin
from book_rental.models.book_publisher import BookPublisher
from generics.views.base_list_view import BaseListView


class PublisherBrowseView(BaseListView, CommonDataMixin):
    template_name = "publisher_browse.html"
    model = BookPublisher

    def get_top_menu(self):
        return "publisher"