from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home),
    path('lsi', views.LSI),
    path('nmf', views.NMF), 
]
