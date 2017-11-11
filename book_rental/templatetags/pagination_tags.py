from django import template

register = template.Library()


@register.filter(name='slice_page_range')
def slice_page_range(page_range, current_page):
    max_index = len(page_range)
    start_index = current_page - 2 if current_page >= 2 else 0
    end_index = current_page + 2 if current_page <= max_index - 2 else max_index
    page_range = list(page_range)[start_index:end_index]
    return page_range


@register.filter(name='first_page')
def first_page(page_range):
    page_range = list(page_range)
    if page_range:
        return page_range[0]


@register.filter(name='last_page')
def last_page(page_range):
    page_range = list(page_range)
    if page_range:
        return page_range[len(page_range) - 1]