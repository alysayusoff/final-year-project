from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.forum, name='forum'),
    path('register/', views.register, name='register'),
    path('login/', views.forum_login, name='forum_login'),
    path('logout/', login_required(login_url='/login/')(views.forum_logout), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/', login_required(login_url='/login/')(views.edit), name='edit'),
    path('post/<int:pk>', views.post, name='post'),
    path('ask/', login_required(login_url='/login/')(views.ask), name='ask'),
    path('search/', views.search, name='search'),
    path('tags/', views.tags, name='tags'),
]