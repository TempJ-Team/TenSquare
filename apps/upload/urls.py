from django.urls import path
from . import views

urlpatterns = [
    path('common/', views.RichEditorImageUpload.as_view()),
    path('avatar/', views.AvatarImageUpload.as_view()),
]
