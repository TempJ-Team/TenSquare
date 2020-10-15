from . import views
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    # 发送短信验证码
    re_path(r'^sms_codes/(?P<mobile>1[3456789]\d{9})/$', views.SendSmscodeView.as_view()),
    # 用户注册
    path('users/', views.UserView.as_view()),
    # 用户登录
    path('authorizations/', obtain_jwt_token),
    # 用户个人中心
    path('user/', views.UserInfoView.as_view()),
    # 修改密码
    path('user/password/', views.ChangePasswordView.as_view()),
    # 关注/取消关注
    re_path(r'^users/like/?P<id>\d+/$', views.FocusUserView.as_view()),
    # 修改个人标签
    path('user/label/', views.ChangeUserLabelView.as_view()),
]
