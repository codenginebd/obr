from ecommerce.models.sales.category import ProductCategory
from generics.views.base_template_view import BaseTemplateView
from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher


class BookSearchView(BaseTemplateView):
    template_name = "book_search.html"

    def get_filter_categories(self):
        cat_id = self.request.GET.get('cat')
        try:
            cat_id = int(cat_id)
        except Exception as exp:
            cat_id = None
        if not cat_id:
            return None, ProductCategory.get_all_parent_categories()
        else:
            parent_cat = ProductCategory.objects.get(pk=cat_id)
            return parent_cat, ProductCategory.get_all_children(cat_id=cat_id)

    def get_filter_authors(self):
        author_objects = Author.objects.all()
        return author_objects

    def get_filter_publisher(self):
        publishers = BookPublisher.objects.all()
        return publishers

    def get_query_params(self, request):
        items = {}
        for key, value in request.GET.items():
            if key == "lang":
                for lang_val in value.split(","):
                    items["lang_%s" % lang_val] = True
            elif key == "rating":
                rating_list = value.split(",")
                try:
                    rating_list = [int(r) for r in rating_list]
                except:
                    rating_list = []
                for r in rating_list:
                    items["rating_%s" % r] = True
            elif key == "use-status":
                use_status_list = value.split(",")
                for u in use_status_list:
                    items["use_status_%s" % u] = True
            elif key == "print-type":
                print_type_list = value.split(",")
                for pt in print_type_list:
                    items["print_type_%s" % pt] = True
            elif key == "out-of-stock":
                items["out_of_stock"] = True
            elif key == "cat":
                items["categories"] = value.split(",")
            elif key == "author":
                items["authors"] = value.split(",")
            elif key == "publisher":
                items["publishers"] = value.split(",")
            else:
                items[key] = value
        return items

    def get_context_data(self, **kwargs):
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['page_title'] = 'Search Books'
        parent_cat, childrens = self.get_filter_categories()
        context['filter_categories'] = childrens
        context["filter_authors"] = self.get_filter_authors()
        context["filter_publishers"] = self.get_filter_publisher()
        context['parent_cat'] = parent_cat
        context["filter_expand"] = self.request.GET.get("cat") or self.request.GET.get("author") or self.request.GET.get("publisher")
        query_params = self.get_query_params(request=self.request)
        context = dict(**context, **query_params)
        return context