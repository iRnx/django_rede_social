from django.contrib import admin
from .models import UserProfile, FriendRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )

    # def friendss(self, obj):
    #     return [r.friends for r in obj.r.all()]
    

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'accepted')
