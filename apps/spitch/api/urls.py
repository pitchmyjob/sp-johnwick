from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ask/(?P<pk>\d+)/spitch/$', NewSpitch.as_view(), name='spitch'),
]