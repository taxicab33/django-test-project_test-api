from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.votes.serializers import VoteSerializer
from votes.views import VotesView


class VoteAPIView(generics.CreateAPIView):
    serializers = VoteSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return VotesView.post(self, request, *args, **kwargs,)

