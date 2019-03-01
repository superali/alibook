from django.contrib import admin
from .models import Profile,FriendRequest
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User=get_user_model()
#admin.site.register( User, UserAdmin)

admin.site.register(Profile)
admin.site.register(FriendRequest)
