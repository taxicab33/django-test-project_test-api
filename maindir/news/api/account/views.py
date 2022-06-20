import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics
from rest_framework.permissions import *

from account.forms import UserEditForm, UserProfileEditForm, UserPasswordEditForm
from account.models import UserProfile
from account.utils import UserMixin
from api.account.serializers import UserSerializer, UserProfileSerializer
from api.newsapp.serializers import ArticleSerializer
from api.newsapp.utils import ArticlesAPIListPagination
from newsapp.model_services import gen_user_slug
from newsapp.utils import DataMixin


class UserArticlesAPIList(generics.ListAPIView, DataMixin):
    serializer_class = ArticleSerializer
    pagination_class = ArticlesAPIListPagination

    def get_queryset(self):
        user = self.get_user()
        articles = self.get_sorted_articles(user=user)
        return articles


class UserInfoAPIView(generics.RetrieveUpdateDestroyAPIView, UserMixin):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        user_info_dict = {
            'user': UserSerializer(user, many=False).data,
            'user_profile': UserProfileSerializer(userprofile, many=False).data
        }
        return HttpResponse(json.dumps(user_info_dict), content_type="application/json")

    def post(self, request, *args, **kwargs):
        context = self.save_user_forms()
        user = context['user']
        userprofile = context['userprofile']
        user_info_dict = {
            'user': UserSerializer(user, many=False).data,
            'user_profile': UserProfileSerializer(userprofile, many=False).data
        }
        return HttpResponse(json.dumps(user_info_dict), content_type="application/json")
