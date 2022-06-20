from rest_framework.routers import Route, SimpleRouter

from .views import *
from rest_framework import routers


# class CustomRouter(SimpleRouter):
#     routes = [
#         Route(
#             url=r'^{prefix}/$',
#             mapping={'get': 'list'},
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         Route(
#             url=r'^{prefix}/{lookup}$',
#             mapping={'get': 'retrieve'},
#             name='{basename}-detail',
#             detail=True,
#             initkwargs={'suffix': 'Detail'}
#         )
#     ]


# router = CustomRouter()
# router.register(r'articles', ArticlesViewSet, basename='articles')
