from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class RichEditorImageUpload(APIView):

    def post(self):
        return Response({'img': '1111'})
