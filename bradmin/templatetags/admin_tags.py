from django import template

register = template.Library()


@register.filter(name='get_item_from_dict_by_key')
def another_filter(dict, key):
    return dict.get(key)