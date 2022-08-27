from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('compiler/', views.compiler, name='compiler'),
    # path('public/<str:room_name>/', views.public, name='public'),
    # path('private/<str:room_name>/', views.private, name='private'),
    path('room/', views.room, name='room'),
]