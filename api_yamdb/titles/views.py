from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from api.mixins import BaseViewSet, ListCreateViewSet
from api.permissions import AdminOrReadOnly
from titles.models import Category, Genre, Title
from titles.serializers import (CategorySerializer, GenreSerializer,
                                TitleSerializer)


class CategoryViewSet(ListCreateViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateViewSet):
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', )

    def get_queryset(self):
        queryset = Title.objects.all()

        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)

        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__slug=category)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        return queryset
