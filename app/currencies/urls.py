from django.urls import path
from . import views

app_name = 'currencies'
urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert, name='convert'),
    path('convertAndDownload/', views.convertAndDownload, name='convertAndDownload'),
]