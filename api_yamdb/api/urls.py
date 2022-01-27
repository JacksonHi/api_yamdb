from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentsViewSet, ReviewViewSet
from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import AdminDataAPI, GetTokenAPI, SignUpAPI, UserDataAPI

router = DefaultRouter()
router.register('users', AdminDataAPI, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
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
