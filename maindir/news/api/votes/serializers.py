from rest_framework import serializers
from votes.models import LikeDislike


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'
