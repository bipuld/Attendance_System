from django.contrib import admin
from .models import *


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['get_user_id', 'get_user_name', 'first_name', 'last_name', 'phone']

    def get_user_name(self, obj):
        return obj.user.email

    def get_user_id(self, obj):
        return obj.user.id

    get_user_name.short_description = 'email'
    get_user_id.short_description = 'ID'
