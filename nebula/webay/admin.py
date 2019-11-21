from django.contrib import admin
from webay.models import UserProfile, Bid, Item, Notification

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Bid)
admin.site.register(Item)
admin.site.register(Notification)
