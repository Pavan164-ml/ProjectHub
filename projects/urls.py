from django.urls import path
from . import views
urlpatterns = [
    path('projects/', views.projects),
    path('project/', views.project),
    path('', views.index)
]