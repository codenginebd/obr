from rest_framework import serializers
from book_rental.models.author import Author
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class AuthorSerializer(BaseModelSerializer):
    cat_id = serializers.SerializerMethodField()

    def get_cat_id(self, obj):
        return [ obj.code ]

    class Meta:
        model = Author
        fields = ('id', 'code', 'name', 'cat_id', 'date_created', 'last_updated')