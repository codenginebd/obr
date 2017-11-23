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
    
    def get_filter_context(self, request, **kwargs):
        author_slug = kwargs.get(self.pk_url_kwarg)
        other_authors = Author.objects.all().exclude(slug=author_slug)
        all_categories = ProductCaategory.objects.all()
        all_publishers = BookPublisher.objects.all()
        selected_categories = request.GET.get('category', None)
        if selected_categories:
            selected_categories = selected_categories.split(",")
            selected_categories = [category.strip() for category in selected_categories if category]
        selected_publishers = request.GET.get('publisher', None)
        if selected_publishers:
            selected_publishers = selected_publishers.split(",")
            selected_publishers = [publisher.strip() for publisher in selected_publishers if publisher]
        exclude_out_of_stock = request.GET.get('exclude_oos', None)
        if exclude_out_of_stock:
            if exclude_out_of_stock == "1":
                exclude_out_of_stock = True
            else:
                exclude_out_of_stock = False
        else:
            exclude_out_of_stock = False
        keyword = request.GET.get('keyword', None)
        if keyword:
            keyword = keyword.strip()
        return {
            'other_authors': other_authors,
            'all_categories': all_categories,
            'all_publishers': all_publishers,
            'selected_categories': selected_categories,
            'selected_publishers': selected_publishers,
            'exclude_out_of_stock': exclude_out_of_stock,
            'keyword': keyword
        }
    
    def get_filter_template(self):
        template_name = "section/author_browse_filter.html"
        return template_name
    