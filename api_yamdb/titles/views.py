from django.shortcuts import get_object_or_404
from rest_framework import filters

from titles.models import Category, Genre, Title
from titles.mixins import ListCreateViewSet
from titles.serializers import CategorySerializer, GenreSerializer


class CategoryViewSet(ListCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ListCreateViewSet):
    queryset = Title.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug',
                     'name', 'year')
