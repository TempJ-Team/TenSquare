from django.urls import path,re_path,include

from . import *

urlpatterns = [

    re_path(r'',include('apps.recruit.urls'))

]
