from rest_framework import serializers

from reviews.models import Comments, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'title')

    def create(self, validated_data):
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
                title=title_id,
                author=self.context['request'].user).exists():
            raise serializers.ValidationError('нельзя оставить отзыв дважды')
        return Review.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('id', 'review')
