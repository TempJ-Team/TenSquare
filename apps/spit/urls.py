from django.urls import path, re_path
from .views import *


urlpatterns = [
    re_path(r'^spit/$', SpitSimpleView.as_view({'get':'list','post':'create'})),
    re_path(r'^spit/(?P<pk>\d+)/$', SpitSimpleView.as_view({'get':'retrieve'})),
    re_path(r'^spit/(?P<pk>\d+)/collect/$', SpitCollectedView.as_view()),
    re_path(r'^spit/(?P<pk>\d+)/updatethumbup/$', SpitHasthumbupView.as_view()),
    re_path(r'^spit/(?P<pk>\d+)/children/$', SpitCommentView.as_view()),
]

