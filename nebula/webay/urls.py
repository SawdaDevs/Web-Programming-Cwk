from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name='webay'

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='webay/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('uploadimage/', views.upload_image, name='uploadimage'),
]