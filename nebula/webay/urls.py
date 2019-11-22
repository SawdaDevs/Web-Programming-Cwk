from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
# will deleteItemView and DeleteView

app_name='webay'

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.auctions, name='auctions'),
    path('item/<int:item_id>/', views.item_view, name='item-detail'),
    path('', views.deleteItem, name='deleteItem'),
    path('auctions/', views.auctions, name='auctions'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='webay/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
]
