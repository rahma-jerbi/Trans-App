from django.urls import path
from . import views

urlpatterns = [
    path('', views.transcriptions, name='transcriptions'),
    path('extract_informations/', views.extract_informations, name='extract_informations'),
]
