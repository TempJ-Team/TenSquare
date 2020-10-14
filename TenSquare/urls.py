from django.urls import re_path, path, include

urlpatterns = [
    re_path(r'', include('apps.article.urls')),
    path('', include('apps.user.urls')),
    re_path(r'',include('apps.recruit.urls')),
    path('upload/', include('apps.upload.urls')),
    re_path('', include(('apps.spit.urls'))),

    path('gatherings/',include('apps.gathering.urls')),
    path('',include('apps.question.urls')),
]
