from django.urls import path
from . import views

urlpatterns = [
    path('common/', views.RichEditorImageUpload.as_view()),
    #    path('admin/', admin.site.urls),
]
