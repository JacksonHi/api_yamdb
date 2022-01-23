from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    
    class meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'post'],
                message='только один review'
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class meta:
        model = Comments
        fields = '__all__'