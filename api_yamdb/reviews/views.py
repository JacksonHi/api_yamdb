from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrAdminOrModerator
from reviews.models import Review, User
from reviews.serializers import CommentsSerializer, ReviewSerializer
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))      
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
