from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from titles.models import Title
from .models import Review, Comments
from .serializers import ReviewSerializer, CommentsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permissions_classes = [
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('...'))
        review = self.request.user.reviews
        # проверка повтора
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permissions_classes = [
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
