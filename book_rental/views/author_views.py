from book_rental.mixin.common_data_mixin import CommonDataMixin
from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from ecommerce.models.sales.category import ProductCategory
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
        author_slug = kwargs.get('slug')
        other_authors = Author.objects.all().exclude(slug=author_slug)
        all_categories = ProductCategory.objects.all()
        all_publishers = BookPublisher.objects.all()
        selected_categories = request.GET.get('category', None)
        if selected_categories:
            selected_categories = selected_categories.split(",")
            selected_categories = [category.strip() for category in selected_categories if category]
        selected_publishers = request.GET.get('publisher', None)
        if selected_publishers:
            selected_publishers = selected_publishers.split(",")
            selected_publishers = [publisher.strip() for publisher in selected_publishers if publisher]
        exclude_out_of_stock = request.GET.get('exclude-oos', None)
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
        rent_available = request.GET.get('rent-available', None)
        if rent_available:
            if rent_available == "1":
                rent_available = True
            else:
                rent_available = False
        else:
            rent_available = False
        color_available = request.GET.get('color-available', None)
        if color_available:
            if color_available == "1":
                color_available = True
            else:
                color_available = False
        else:
            color_available = False
        ori_available = request.GET.get('ori-available', None)
        if ori_available:
            if ori_available == "1":
                ori_available = True
            else:
                ori_available = False
        else:
            ori_available = False
        eco_available = request.GET.get('eco-available', None)
        if eco_available:
            if eco_available == "1":
                eco_available = True
            else:
                eco_available = False
        else:
            eco_available = False
        return {
            'other_authors': other_authors,
            'all_categories': all_categories,
            'all_publishers': all_publishers,
            'selected_categories': selected_categories,
            'selected_publishers': selected_publishers,
            'exclude_out_of_stock': exclude_out_of_stock,
            'keyword': keyword,
            'rent_available': rent_available,
            'color_available': color_available,
            'ori_available': ori_available,
            'eco_available': eco_available
        }
    
    def get_filter_template(self):
        template_name = "sections/author_browse_filter.html"
        return template_name
    