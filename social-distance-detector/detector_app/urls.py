from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # For the main webpage
    path('video_feed', views.video_feed, name='video_feed'), # For the video stream
]