from django.urls import re_path

from . import consumers
from group import consumers as group_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<pv_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/group/(?P<group_id>\w+)/$', group_consumers.GroupConsumer.as_asgi()),
]