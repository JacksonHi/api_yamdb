from rest_framework import filters

from titles.models import Category, Genre, Title
from titles.mixins import BaseViewSet
from titles.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)
from titles.permissions import AdminOrReadOnly


class CategoryViewSet(BaseViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(BaseViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug',
                     'name', 'year')
