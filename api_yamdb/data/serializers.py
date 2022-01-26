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
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'category', 'genre']

    def create(self, validated_data):

        current_category = None
        if 'category' in self.initial_data:
            category = self.initial_data.get('category')
            try:
                current_category = Category.objects.get(slug=category)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    'Переданые некорректные данные Category'
                )

        title = Title.objects.create(category=current_category,
                                     **validated_data)

        genres = []
        if 'genre' in self.initial_data:
            genres = self.initial_data.getlist('genre')

        for genre in genres:
            try:
                current_genre = Genre.objects.get(slug=genre)
            except Genre.DoesNotExist:
                raise serializers.ValidationError(
                    f'Переданые некорректные данные Genre {genre}'
                )
            title.genre.add(current_genre)

        return title

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )

        current_category = None
        if 'category' in self.initial_data:
            category = self.initial_data.get('category')
            try:
                current_category = Category.objects.get(slug=category)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    'Переданые некорректные данные Category'
                )
        instance.category = current_category
        instance.save()

        genres = []
        if 'genre' in self.initial_data:
            instance.genre.delete()
            genres = self.initial_data.getlist('genre')

        for genre in genres:
            try:
                current_genre = Genre.objects.get(slug=genre)
            except Genre.DoesNotExist:
                raise serializers.ValidationError(
                    f'Переданые некорректные данные Genre {genre}'
                )
            instance.genre.add(current_genre)
        return instance


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
        fields = ('id', 'text', 'author', 'pub_date')
