from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView,ListAPIView
from rest_framework.response import Response

from utils.paginations import MyPage
from .serialziers import SpitSimpleSerializer
from .models import Spit
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class SpitSimpleView(ModelViewSet):
    queryset = Spit.objects.all()
    serializer_class = SpitSimpleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('id')
        if keyword:
            return self.queryset.filter(order_id__contains=keyword)
        return self.queryset.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        _data = request.data
        if user.is_authenticated:
            _data['user_id'] = user.id
            _data['nickname'] = user.nickname
            _data['avatar'] = user.avatar
        else:
            _data['user_id'] = None
            _data['nickname'] = None
            _data['avatar'] = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpitCollectView(UpdateAPIView):
    queryset = Spit.objects.all()
    serializer_class = SpitSimpleSerializer
    pagination_class = MyPage


class SpitHasthubupView(UpdateAPIView):
    queryset = Spit.objects.all()
    serializer_class = SpitSimpleSerializer
    pagination_class = MyPage

