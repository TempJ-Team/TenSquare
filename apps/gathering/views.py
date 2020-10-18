from datetime import datetime
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Gathering
from .serializer import GatheringsSerializer, GatherSerializerSimple
from utils.paginations import MyPage


# 获取所有活动
class Gatherings(ListAPIView):
    queryset = Gathering.objects.filter(state=1)
    serializer_class = GatherSerializerSimple
    pagination_class = MyPage


# 获取某个活动详情
class GatheringView(RetrieveAPIView):
    queryset = Gathering.objects.filter(state=1)
    serializer_class = GatheringsSerializer


# 参加或取消某个活动
class GatherJoinView(GenericAPIView):
    queryset = Gathering.objects.filter(state=1)
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        # 返回详情视图所需的模型类数据对象
        gathering = self.get_object()
        nowtime = datetime.now()
        endtime = gathering.endrolltime.replace(tzinfo=None)
        if endtime < nowtime:
            return Response({'success': False, 'message': '报名时间已过'}, status=400)
        else:
            if user in gathering.users.all():
                gathering.users.remove(user)
                gathering.save()
                return Response({'success': True, 'message': '取消成功'})
            else:
                gathering.users.add(user)
                gathering.save()
                return Response({'success': True, 'message': '参加成功'})
