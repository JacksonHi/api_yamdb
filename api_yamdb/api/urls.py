from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserDataAPI, AdminDataAPI


router = DefaultRouter()
router.register('users', AdminDataAPI, basename='users')

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserDataAPI.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
