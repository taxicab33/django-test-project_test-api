from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.favorite.serializers import FavoriteSerializer
from favorites.views import favorite


class FavoriteAPIView(generics.CreateAPIView):
    serializers = FavoriteSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return favorite(request, **kwargs)
