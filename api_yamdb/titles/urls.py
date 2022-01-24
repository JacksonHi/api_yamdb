from django.conf.urls import url
from django.urls import include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

app_name = 'titles'
urlpatterns = [
    url('v1/', include(router.urls)),
]
