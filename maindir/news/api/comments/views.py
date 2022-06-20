import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from api.comments.serializers import CommentSerializer
from comments.models import Comment
from comments.views import CommentView
from newsapp.models import Article


class CommentAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        print(kwargs)
        return CommentView.post(self, request, *args, **kwargs)


class CommentsAPIList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        content_type = ContentType.objects.get(model=self.request.query_params.get('content_type'))
        object_id = self.request.query_params.get('object_id')
        return Comment.objects.filter(object_id=object_id, content_type=content_type)