from rest_framework import serializers
from newsapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    views = serializers.HiddenField(default=0)
    likes = serializers.HiddenField(default=0)
    dislikes = serializers.HiddenField(default=0)
    rating = serializers.HiddenField(default=0)

    class Meta:
        model = Article
        exclude = ('slug', )
