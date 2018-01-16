from django.urls import path
from . import views

app_name = 'currencies'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('convert/', views.ConvertView.as_view(), name='convert'),
    path('convertAndDownload/', views.ConvertAndDownloadView.as_view(), name='convert_and_download'),
]