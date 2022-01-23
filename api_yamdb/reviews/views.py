from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from titles.models import Title
from .models import Review, Comments
from .serializers import ReviewSerializer, CommentsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
    
    def get_queryset(self):
        print("хз1")
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        print("хз")
        return title.reviews.all()



class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
