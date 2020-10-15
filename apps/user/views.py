from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from utils.celery_tasks.sms.tasks import send_sms_code
import re
from random import randint
from django_redis import get_redis_connection

from .serializers import UserModelSerializer, User, ChangePasswordModelSerializer, UserInfoSerializer, ChangeLabelModelSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.generics import UpdateAPIView

from apps.question.models import Label

# 获取短信验证码
class SendSmscodeView(APIView):
    def get(self, request, mobile):
        if not re.match('^1[3456789]\d{9}$', mobile):
            return Response(data='手机号码格式错误', status=status.HTTP_400_BAD_REQUEST)

        sms_code = '%06d' % randint(0, 999999)

        conn = get_redis_connection('verify_code')
        if conn.get('flag_%s' % mobile):
            return Response(data='不可重复发送短信', status=status.HTTP_400_BAD_REQUEST)

        send_sms_code.delay(mobile, sms_code)
        try:
            conn.setex(
                'sms_%s' % mobile,
                300,
                sms_code
            )
            conn.setex(
                'flag_%s' % mobile,
                60,
                1
            )
        except Exception as e:
            return Response(data='短信验证码写入缓存失败', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={
            'success': True,
            'sms_code': sms_code,
            'message': '短信发送成功'
        })


# 用户注册--颁发token
class UserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def post(self, request, *args, **kwargs):
        # 校验短信验证码
        sms_code = request.data['sms_code']
        mobile = request.data['mobile']

        conn = get_redis_connection('verify_code')
        sms_code_from_redis = conn.get('sms_%s' % mobile)
        if not sms_code_from_redis:
            return Response(data='短信验证码不存在', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if sms_code != sms_code_from_redis.decode():
            return Response(data='短信验证码不正确', status=status.HTTP_400_BAD_REQUEST)

        # 实例化序列化器
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # 注册成功添加状态保持--使用jwt
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({
            'id': user.id,
            'username': user.username,
            'mobile': user.mobile,
            'avatar': user.avatar,
            'token': token
        })


# 用户个人中心
class UserInfoView(RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user


# 修改密码
class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# 关注用户/取消关注
class FocusUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = lookup_field

    def post(self, request, id):
        user = self.request.user
        idol_user = self.get_object()

        try:
            user.idols.add(idol_user)
            # idol_user.fans.add(user)  # 这两个随便选择一个操作即可
        except Exception as e:
            return Response(data='关注用户失败', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'success': 'true',
                'message': '关注用户成功'
            })

    def delete(self):
        user = self.request.user
        idol_user = self.get_object()

        try:
            user.idols.remove(idol_user)
            # idol_user.fans.add(user)  # 这两个随便选择一个操作即可
        except Exception as e:
            return Response(data='取消关注用户失败', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'success': 'true',
                'message': '取消关注用户成功'
            })


# 修改用户标签
class ChangeUserLabelView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeLabelModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        labels_list = request.data['labels']
        user = self.get_object()

        user.labels.set(labels_list)

        return Response({
            'success': 'true',
            'message': '标签修改成功'
        })


# 第三方登录--qq






























