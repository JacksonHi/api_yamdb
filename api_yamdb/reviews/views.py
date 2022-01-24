from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from titles.models import Title
from .models import Review
from .serializers import ReviewSerializer, CommentsSerializer
from .permissions import IsAuthorOrAdminOrModerator


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    """def retrieve(self, request, *args, **kwargs):
        revi = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        serializer = ReviewSerializer(revi)
        return Response(serializer.data)"""


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
