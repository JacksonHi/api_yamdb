from django.contrib.auth import get_user_model
from rest_framework import serializers

from titles.models import Category, Genre, Title

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
