from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from bauth.models.user import BUser


def validate_phone_number(value):
    if not all([True for i in value if i >= '0' and i <= '9']) and len(value) != 10:
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )
    else:
        if BUser.objects.filter(phone=value).exists():
            raise ValidationError(
                _('%(value)s already used'),
                params={'value': value},
            )
