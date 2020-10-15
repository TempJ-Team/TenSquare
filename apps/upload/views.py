from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from utils.Qiniu_utils import imAge_upload
# from config.config import URL
from rest_framework import status
from config.config import eXt_List


# Create your views here.

class RichEditorImageUpload(APIView):

    def post(self, request):
        _img = request.data.get('upload')
        if _img:
            ext = _img.name.split('.')[-1]
            if ext not in eXt_List:
                return Response({
                    'msg': '文件类型不允许！'
                }, status=status.HTTP_400_BAD_REQUEST)

        image_url = imAge_upload(_img)
        callback = '127.0.0.1:8080'
        if image_url:
            return redirect('http://'+callback+'/upload_success.html?image_url='+image_url+'&CKEditorFuncNum=1')
        return Response({
            'msg': '服务器内部错误！'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AvatarImageUpload(APIView):

    def post(self, request):
        _img = request.data.get('img')
        if _img:
            ext = _img.name.split('.')[-1]

            if ext not in eXt_List:
                return Response({
                    'msg': '文件类型不允许！'
                }, status=status.HTTP_400_BAD_REQUEST)

        image_url = imAge_upload(_img)

        if image_url:
            return Response({
                'imgurl': image_url,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'msg': '服务器内部错误！'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
