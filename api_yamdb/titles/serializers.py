from django.contrib.auth import get_user_model
from rest_framework import serializers

from titles.models import Category, Genre, Title, TitleGenre

User = get_user_model()


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
        fields = '__all__'

    def create(self, validated_data):

        current_category = None
        if 'category' in self.initial_data:
            category = self.initial_data.get('category')
            current_category, status = Category.objects.get_or_create(name=category)
        title = Title.objects.create(category=current_category,**validated_data)

        genres = []
        if 'genre' in self.initial_data:
            genres = self.initial_data.get('genre')

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(name=genre)
            TitleGenre.objects.create(genre=current_genre, title=title)

        return title
