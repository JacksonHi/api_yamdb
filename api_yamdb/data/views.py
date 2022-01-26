from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import ReviewSerializer, CommentsSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAuthorOrAdminOrModerator, IsAdmin, AdminOrReadOnly, IsAdminPe, OwnResourcePermission, IsAdminOrReadOnly, IsAuthorOrModerator

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import filters, status, permissions, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import AdminSerializer, StandartUserSerializer, TokenSerializer, CategorySerializer, GenreSerializer, TitleSerializer
from .mixins import BaseViewSet, ListCreateViewSet
from reviews.models import Title, Review, Category, Genre, Title, User



class SignUpAPI(APIView):
    """Запрос на регистрацию"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = StandartUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data['username'])
            verification_code = default_token_generator.make_token(user)
            send_mail(
                subject='Verificate registration on YaMDB',
                message=f'Verificate your email clicking {verification_code}',
                from_email='master@yamdb.com',
                recipient_list=(serializer.data['email'],),
            )
            return Response(
                {'email': serializer.data['email'],
                 'username': serializer.data['username']},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPI(APIView):
    """Запрос на получение токена"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=serializer.data['username'])
            if default_token_generator.check_token(user, serializer.data['verification_code']):
                access_token = AccessToken.for_user(user)
                return Response(
                    {'token': str(access_token)}, status=status.HTTP_200_OK
                )
        return Response({'verification_code': 'Invalid verification code'},status=status.HTTP_400_BAD_REQUEST)


class UserDataAPI(APIView):
    """Обычный пользователь работает со своими данными"""
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(user, many=False, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDataAPI(ModelViewSet):
    """Админ работает с данными пользователя"""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = (IsAdminOrReadOnly | IsAuthorOrModerator,)
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id',))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id',))
        reviews = self.request.user.reviews
        if reviews.filter(title=title).exists():
            raise serializers.ValidationError(
                detail="Вы уже делали ревью на это произведение!",
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()