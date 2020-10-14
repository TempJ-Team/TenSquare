from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from utils.paginations import MyPage
from .serialziers import *
from .models import Spit
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views import View
from django.http import JsonResponse




class SpitSimpleView(ModelViewSet):
    queryset = Spit.objects.all()
    serializer_class = SpitSimpleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = MyPage

    # def get_queryset(self):
    #     keyword = self.request.query_params.get('id')
    #     if keyword:
    #         return self.queryset.filter(id=keyword)
    #     return self.queryset.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        _data = request.data
        _data['userid'] = user.id
        _data['nickname'] = user.nickname
        _data['avatar'] = user.avatar

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        print(instance)
        parent = instance.parent
        print(instance.parent)
        if parent:
            parent.comment +=1
            parent.save()

    # def get(self,request,*agrs,**kwargs):
    #     query = Spit.objects.filter(parent__isnull=True).order_by('id')
    #     serializer = SpitSimpleSerializer(query,many=True)
    #
    #     return  Response(data=serializer.data)


class SpitCollectView(View):
    def put(self, request,id):
        spit = Spit.objects.get(pk=id)
        if spit.collected==True:
            spit.collected = False
            spit.save()
        else:
            spit.collected = True
            spit.save()
        return JsonResponse({
            'message':'ok',
            'success':'spit.collected'
        })



class SpitHasthubupView(View):
    def put(self, request,id):
        spit = Spit.objects.get(pk=id)
        if spit.hasthumbup==True:
            spit.hasthumbup = False
            spit.thumbup += 1
            spit.save()
        else:
            spit.hasthumbup = True
            spit.thumbup -= 1
            spit.save()
        return JsonResponse({
            'message':'ok',
            'success':'spip.hasthumbup'
        })


class SpitCommentView(RetrieveAPIView):
    queryset = Spit.objects.all()
    # queryset = Spit.objects.filter(parent__in='pk').all()
    serializer_class = SpitCommentSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        # instance = self.get_object()
        queryset = Spit.objects.filter(parent__in=pk).all()
        serializer = self.get_serializer(instance=queryset,many=True)
        return Response(serializer.data)
