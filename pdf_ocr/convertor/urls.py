from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='convertor-home'),
    path('download', views.download, name='download'),
]