from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserDataAPI, AdminDataAPI
from .views import ReviewViewSet, CommentsViewSet, GetTokenAPI, SignUpAPI, CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register('users', AdminDataAPI, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/users/me/', UserDataAPI.as_view(), name='me'),
    path('v1/auth/signup/', SignUpAPI.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenAPI.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
