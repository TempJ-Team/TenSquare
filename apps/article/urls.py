from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^channels/$', views.ChannelViews.as_view({'get': 'list'}))
]
