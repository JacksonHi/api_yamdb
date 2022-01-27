from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrAdminOrModerator
from reviews.models import Review
from reviews.serializers import CommentsSerializer, ReviewSerializer
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
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

        agg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = agg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        agg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = agg_score['score__avg']
        title.save(update_fields=['rating'])


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
