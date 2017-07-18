from django import template
from settings import FACEBOOK_APP_ID

register = template.Library()


@register.filter(name='facebook_app_id')
def get_modules(config):
    return FACEBOOK_APP_ID
