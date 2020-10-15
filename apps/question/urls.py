from django.urls import path,re_path
from apps.question.views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    re_path(r'^authorizations/$',obtain_jwt_token),
    re_path(r'^labels/$', LabelView.as_view({'get':'list'})),#1.所有标签列表
    re_path(r'^labels/users/$',LabelView.as_view({'get':'latest'})),#2.用户关注的标签
    re_path(r'^questions/(?P<id>-?[1-9]\d*)/label/new/$',QuestionView.as_view()),#3.最新问题
    re_path(r'^questions/(?P<id>-?[1-9]\d*)/label/hot/$',HotquestionView.as_view()),#4.最热问题
    re_path(r'^questions/(?P<id>-?[1-9]\d*)/label/wait/$', WiatquestionView.as_view()),#5.等待问题
    re_path(r'^questions/$',ReleasequestionView.as_view()),#6.发布问题
    re_path(r'^questions/(?P<pk>-?[0-9]\d*)/$', QuestiondetailsView.as_view({'get':'retrieve'})),#7.问题详情
    re_path(r'^questions/(?P<pk>-?[0-9]\d*)/useful/$',UsefulQuestionView.as_view()),#8.问题有用
    re_path(r'^questions/(?P<pk>-?[0-9]\d*)/unuseful/$',UnusefulQuestionView.as_view()),#9.问题没用
    re_path(r'^reply/$',ReplyView.as_view()),#10.回答问题
    re_path(r'^reply/(?P<pk>-?[0-9]\d*)/useful/$', UsefulQView.as_view()),#11.问题有用
    re_path(r'^reply/(?P<pk>-?[0-9]\d*)/unuseful/$', UnusefulQView.as_view()),#12.问题没用
    re_path(r'^labels/(?P<pk>-?[0-9]\d*)/focusin/$', AttentionstagsView.as_view()),#13.关注标签
    re_path(r'^labels/(?P<pk>-?[0-9]\d*)/focusout/$', AttentiontagsView.as_view()),#14.关注标签
    re_path(r'^labels/(?P<pk>-?[0-9]\d*)/$', TagsView.as_view({'get':'retrieve'})),#15.标签详情
    re_path(r'^labels/full/$', LabelFullView.as_view()),




    # re_path(r'^questions/\d+/$',QuestiondetailsView.as_view()),

]