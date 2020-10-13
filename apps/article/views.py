from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from .pageations import MyPage


class ChannelViews(ModelViewSet):
    queryset = Channel.objects.filter()
    serializer_class = ChannelModelSerializer
    pagination_class = MyPage


