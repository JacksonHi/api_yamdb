from rest_framework import serializers, exceptions, validators
from rest_framework.validators import UniqueValidator

from reviews.models import Review, Comments, User, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', ' first_name', 'last_name', 'role')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    verification_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'There is no user {value}')
        return value

    
class AdminSerializer(serializers.ModelSerializer):
    """Роль admin."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


class StandartUserSerializer(serializers.ModelSerializer):
    """Роль user."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    #title = serializers.SlugRelatedField(queryset=Title.objects.all(), slug_field='id')
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        """validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='нельзя оставить отзыв дважды'
            )
        ]"""


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
