import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views import View

from comments.services import get_object, comment_action
from newsapp.models import Article
from comments.models import Comment


class CommentView(View, LoginRequiredMixin):
    model = None

    def post(self, request, **kwargs):
        json_dict = comment_action(request)
        return HttpResponse(json.dumps(json_dict), content_type="application/json")

