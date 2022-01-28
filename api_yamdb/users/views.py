from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import FROM_EMAIL
from users.models import User
from users.serializers import (AdminSerializer, StandartUserSerializer,
                               TokenSerializer)


class SignUpAPI(APIView):
    """Запрос на регистрацию"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = StandartUserSerializer(data=request.data)
        # через try-except все валится из-за того, что я вызываю
        # serializer.save() без проверки is_valid
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        user, was_created = User.objects.get_or_create(
            email=serializer.data['email'],
        )
        if not was_created:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user, was_created = User.objects.get_or_create(
            username=serializer.data['username'],
        )
        if not was_created:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        verification_code = default_token_generator.make_token(user)
        send_mail(
            subject='Verificate registration on YaMDB',
            message=f'Verificate your email clicking {verification_code}',
            from_email=FROM_EMAIL,
            recipient_list=(serializer.data['email'],),
        )
        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username']},
            status=status.HTTP_200_OK
        )


class GetTokenAPI(APIView):
    """Запрос на получение токена"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        user = get_object_or_404(
            User, username=serializer.data['username'])
        if default_token_generator.check_token(
                user, serializer.data['verification_code']):
            access_token = AccessToken.for_user(user)
            return Response(
                {'token': str(access_token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'verification_code': 'Invalid verification code'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDataAPI(APIView):
    """Обычный пользователь работает со своими данными"""
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(
            user, many=False, partial=True, data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminDataAPI(ModelViewSet):
    """Админ работает с данными пользователя"""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
