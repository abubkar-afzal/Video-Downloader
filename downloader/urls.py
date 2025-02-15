from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('youtube/', views.download_youtube, name='youtube'),
    path('instagram/', views.download_instagram, name='instagram'),
    path('progress/', views.get_progress, name='progress'),
]
