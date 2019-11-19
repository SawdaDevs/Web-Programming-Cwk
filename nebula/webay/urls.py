from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from .views import ItemDetailView

app_name='webay'

urlpatterns = [
    path('', views.index, name='index'),
    path('auctions/', views.auctions, name='auctions'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='webay/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    
]
