from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^feed/$', FeedListApiView.as_view(), name='feed'),
]
