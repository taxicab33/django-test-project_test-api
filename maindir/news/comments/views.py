import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from comments.models import Comment
from comments.services import comment_action


class CommentView(View, LoginRequiredMixin):
    model = Comment

    def post(self, request, *args, **kwargs):
        json_dict = comment_action(request)
        return HttpResponse(json.dumps(json_dict), content_type="application/json")

