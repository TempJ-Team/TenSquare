from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from utils.paginations import MyPage
from .serialziers import *
from .models import Spit
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class SpitSimpleView(ModelViewSet):
    queryset = Spit.objects.all()
    serializer_class = SpitSimpleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = MyPage

    def list(self, request, *args, **kwargs):
        queryset = Spit.objects.filter(parent__id=None).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        _data = request.data

        _data['userid'] = user.id
        _data['nickname'] = user.username
        _data['avatar'] = user.avatar

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        parent = instance.parent
        if parent:
            parent.comment += 1
            parent.save()

    # @action(methods=['put'], detail=True)
    # def updatehastumbup(self, request,id):
    #     spit = Spit.objects.get(pk=id)
    #     if spit.hasthumbup==True:
    #         spit.hasthumbup = False
    #         spit.thumbup += 1
    #         spit.save()
    #     else:
    #         spit.hasthumbup = True
    #         spit.thumbup -= 1
    #         spit.save()
    #     return Response({
    #         'message':'ok',
    #         'success':'spit.hasthumbup'
    #     })


class SpitCollectedView(UpdateAPIView):
    queryset = Spit.objects.all()
    serializer_class = SpitCollectedSerializer

    def put(self, request, pk, *args, **kwargs):
        user = self.request.user
        spit = Spit.objects.get(pk=pk)

        if user not in spit.collected_users.all():
            spit.collected_users.add(user)
            spit.collected = True
            spit.save()
            return Response({
                'message': '收藏成功',
                'success': True
            })
        else:
            spit.collected_users.remove(user)
            spit.collected = False
            spit.save()
            return Response({
                'message': '取消收藏成功',
                'success': True
            })

class SpitHasthumbupView(UpdateAPIView):
    queryset = Spit.objects.all()
    serializer_class = SpithasthumbupSerializer

    def put(self, request, pk, *args, **kwargs):
        user = self.request.user
        spit = Spit.objects.get(pk=pk)

        if user not in spit.collected_users.all():
            spit.hasthumbup_users.add(user)
            spit.hasthumbup = True
            spit.thumbup += 1
            spit.save()
            return Response({
                'message': '收藏成功',
                'success': True
            })
        else:
            spit.hasthumbup_users.remove(user)
            spit.hasthumbup = False
            spit.thumbup -= 1
            spit.save()
            return Response({
                'message': '取消收藏成功',
                'success': True
            })
    #
    # @action(methods=['put'],detail=True)
    # def collect(self,request,id):
    #     spit = Spit.objects.get(pk=id)
    #     if spit.collected == True:
    #         spit.collected = False
    #         spit.save()
    #     else:
    #         spit.collected = True
    #         spit.save()
    #     return Response({
    #         'message':'ok',
    #         'success':'spit.collected'
    #     })

    #


class SpitCommentView(RetrieveAPIView):
    queryset = Spit.objects.all()
    serializer_class = SpitCommentSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = Spit.objects.filter(parent__id=pk).all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
