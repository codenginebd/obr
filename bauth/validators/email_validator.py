import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email(value):
    if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", value):
        raise ValidationError(
            _('%(value)s is not a valid email address'),
            params={'value': value},
        )
    else:
        if User.objects.filter(username=value).exists():
            raise ValidationError(
                _('%(value)s already used'),
                params={'value': value},
            )