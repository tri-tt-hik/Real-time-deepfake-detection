from django.urls import path
from . import views

urlpatterns = [
    path('fetch-results/', views.fetch_results, name='fetch_results'),
    path("home/", views.home, name="home"),
    path("video/", views.video, name="video"),
    path("stream/", views.stream, name="stream"),
    path("history/", views.history, name="history"),
    path("real/", views.real, name="real"),
]