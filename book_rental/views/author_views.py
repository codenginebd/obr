from book_rental.mixin.common_data_mixin import CommonDataMixin
from generics.views.base_template_view import BaseTemplateView


class AuthorBrowseView(BaseTemplateView, CommonDataMixin):
    template_name = "author_browse.html"