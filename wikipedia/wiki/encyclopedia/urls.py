from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.topic, name="topic"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("wiki/", views.randomq, name="randomq"),
    path("edit/<str:entry>", views.edit, name="edit")
  
    
]