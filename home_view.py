from bauth.decorators.authentication import UserLoginRequired
from book_rental.mixin.common_data_mixin import CommonDataMixin
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.front_list import FrontList
from ecommerce.models.sales.list_group import ListGroup
from generics.views.base_template_view import BaseTemplateView


class HomeView(BaseTemplateView, CommonDataMixin):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page_title'] = 'Buy, Sale, Rent Books Online | bdreads.com'

        slug = kwargs.get('slug')

        category_object = None

        if slug:
            slug = slug.split('/')[-1:]
            if slug:
                slug = slug[0]

                category_objects = ProductCategory.objects.filter(slug=slug)
                category_object = category_objects.first()

        if not slug:
            context["filter_category_show"] = True
            context["linkable"] = False
            context["filter_category_header"] = "All Categories"
            childrens = self.get_all_parent_categories()
            context["filter_categories"] = childrens
            if len(childrens) > 10:
                context["show_search"] = True
            else:
                context["show_search"] = False
        else:
            if category_object:
                context["filter_category_show"] = True
                context["linkable"] = True
                context["slug"] = category_object.slug
                context["filter_category_header"] = category_object.name
                childrens = self.get_all_children(cat_id=category_object.pk)['children']
                if childrens:
                    context["filter_categories"] = childrens
                else:
                    context["filter_category_show"] = False

                if len(childrens) > 10:
                    context["show_search"] = True
                else:
                    context["show_search"] = False
            else:
                context["filter_category_show"] = False

        context['header_categories'] = self.get_all_categories()
        context["header_authors"] = self.get_all_authors()
        context["header_publishers"] = self.get_all_publishers()

        # Front List
        front_lists = []
        groups = ListGroup.objects.filter(is_active=True)
        for group in groups:
            group_list = {}
            flists = FrontList.objects.filter(is_active=True, group_id=group.pk)
            for flist in flists:
                group_list[flist.name] = {
                    ''
                }

        return context