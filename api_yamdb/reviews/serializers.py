from rest_framework import serializers

from .models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = ...
    title = ...
    
    class meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    author = ...
    review = ...

    class meta:
        model = Comments
        fields = '__all__'