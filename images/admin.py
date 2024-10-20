from django.contrib import admin
from .models import Picture, UserInfo

# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_agent', 'ip', 'time', 'picture', 'message_id', 'user_id']

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'title', 'format', 'image']
