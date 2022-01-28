from rest_framework import serializers, validators

from reviews.models import Comments, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title',)

        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='нельзя оставить отзыв дважды'
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
