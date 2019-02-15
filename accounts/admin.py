from django.contrib import admin
from .models import Profile,FriendRequest
from django.contrib.auth.admin import UserAdmin
#from .models import  User
#admin.site.register( User, UserAdmin)

admin.site.register(Profile)
admin.site.register(FriendRequest)
