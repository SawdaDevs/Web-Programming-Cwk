from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
# will deleteItemView and DeleteView

app_name='webay'

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.auctions, name='auctions'),
    path('item/<int:item_id>/', views.item_view, name='item-detail'),
    path('deleteItem/<int:item_id>', views.deleteItem, name='deleteItem'),
    path('bidItem/<int:item_id>', views.bidItem, name='bidItem'),
    path('openauctions/', views.auctions, name='auctions'),
    path('closedauctions/',views.closed_auctions, name='closedauctions'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('getUserDetails/', views.get_user_details, name='get_user_details'),
    path('updateProfile/', views.update_profile_details, name='update_profile_details'),
    path('updateProfilePic/', views.update_profile_pic, name='update_profile_pic'),
    path('getNotifications/', views.get_notifications, name='get_messages'),
    path('getNotificationMessage/<int:id>', views.get_notifications_message, name='get_notifications_message'),
    path('markNotificationAsRead/<int:id>', views.mark_notification_as_read, name='mark_notif_read'),
    path('getUnreadNotifNumber/', views.get_number_unread_notifs, name='get_number_unread_notifs'),
    path('notifications/', views.display_notifications, name='display_notifications'),
    path('login/', auth_views.LoginView.as_view(template_name='webay/login.html'), name='login'),
    path('logout/', views.logout, name="logout"),
    path('additem/', views.add_item, name='additem'),
    path('search/', views.search, name='search'),
]
