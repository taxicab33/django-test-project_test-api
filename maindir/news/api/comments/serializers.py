from django.utils import timezone
from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    views = serializers.HiddenField(default=0)
    likes = serializers.HiddenField(default=0)
    dislikes = serializers.HiddenField(default=0)
    rating = serializers.HiddenField(default=0)

    class Meta:
        model = Comment
        exclude = ('content_type', 'object_id', 'parent')
