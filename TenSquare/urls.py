from django.urls import re_path, path, include

urlpatterns = [
    re_path(r'', include('apps.article.urls')),
    path('', include('apps.user.urls')),
    re_path(r'',include('apps.recruit.urls')),
]
