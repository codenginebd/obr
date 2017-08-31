from django.core.urlresolvers import reverse
from book_rental.models.author import Author
from generics.api.serializers.base_model_serializer import BaseModelSerializer
from rest_framework import serializers


class AuthorSerializer(BaseModelSerializer):
    link = serializers.SerializerMethodField()
    
    def get_link(self, obj):
        return ""

    class Meta:
        model = Author
        fields = ('id', 'code', 'name', 'link', 'date_created', 'last_updated')