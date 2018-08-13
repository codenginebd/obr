from book_rental.models import Book
from generics.views.base_detail_view import BaseDetailView


class BookDetailsView(BaseDetailView):
    model = Book
    template_name = "book_details.html"

    def get_page_title(self):
        return "Book Details - %s | Online Book Rental Services" % self.object.get_title()
