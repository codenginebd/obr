from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class BRPaginationMixin(object):

    def make_pagination(self, request, queryset, page_size=20, *args, **kwargs):
        self.paginator = Paginator(queryset, page_size)

        page_num = request.GET.get('page')
        try:
            page_num = int(page_num)
            self.page = self.paginator.page(page_num)
        except PageNotAnInteger:
            self.page = self.paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            self.page = queryset.model.objects.none()