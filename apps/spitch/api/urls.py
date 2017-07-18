from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ask/(?P<pk>\d+)/spitch/$', NewSpitch.as_view(), name='spitch'),
    url(r'^ask/(?P<pk>\d+)/swipe/$', ListSwipeSpitch.as_view(), name='swipe-spitch'),
    url(r'^spitch/(?P<pk>\d+)/$', RetrieveSpitch.as_view(), name='spitch-retrieve'),
    url(r'^like/$', LikeSpitch.as_view(), name='spitch-like'),
]