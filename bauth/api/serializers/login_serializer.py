from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from bauth.models.user import BUser

__author__ = 'Codengine'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    class Meta:
        model = User
