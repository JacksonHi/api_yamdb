from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination


class BaseViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination



class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    # permission_classes = (permissions.IsAuthenticated,)


class ListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
