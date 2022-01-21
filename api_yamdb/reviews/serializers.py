from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    
    class meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = ...

    class meta:
        model = Comments
        fields = '__all__'