from django.urls import path, re_path
from .views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # re_path(r'^search/$', views.MySearchView()),
    re_path(r'^spit/$', SpitSimpleView.as_view({'get':'list','post':'create'})),
    re_path(r'^spit/(?P<pk>\d+)/$', SpitSimpleView.as_view({'get':'retrieve'})),
    re_path(r'^spit/(?P<id>\d+)/collect/$', SpitCollectView.as_view()),
    re_path(r'^spit/(?P<id>\d+)/updatethumbup/$', SpitHasthubupView.as_view()),
    re_path(r'^spit/(?P<pk>\d+)/children/$', SpitCommentView.as_view()),
    # re_path(r'^authorizations/$', obtain_jwt_token),
]

