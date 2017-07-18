from django import template

register = template.Library()


@register.filter(name='slug_url_from_dict')
def slug_url_from_dict(slug_dict, cat_id): # Only one argument.
    return slug_dict.get(cat_id)


@register.filter(name='has_any_children')
def has_any_children(item_id, parent_dict):
    return parent_dict.get(item_id)