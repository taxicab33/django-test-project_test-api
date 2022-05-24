import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render

from favorites.models import Favorite
from newsapp.models import Article
from votes.services import get_object


@login_required
def favorite(request, **kwargs):
    result = bool
    if request.user.is_authenticated:
        obj = get_object(request)
        content_type = ContentType.objects.get_for_model(obj)
        try:
            fav = Favorite.objects.get(content_type=content_type, object_id=obj.id, user=request.user)
            fav.delete()
            result = False
        except Favorite.DoesNotExist:
            Favorite.objects.create(user=request.user, object_id=obj.id, content_type=content_type)
            result = True
    return HttpResponse(json.dumps({
            "result": result
        }), content_type="application/json")
