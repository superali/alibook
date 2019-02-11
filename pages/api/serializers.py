from django.utils.timesince import timesince
from rest_framework import serializers

from pages.models import Page
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer

class PageModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    verb_like = serializers.SerializerMethodField()
    class Meta:
        model=Page
        fields=[
                'id','user',
                'content','name','created_at',
                'likes','did_like','verb_like',
                ]
     
    def get_did_like(self,obj):
        request = self.context.get("request")
        try:
            if request.user.is_authenticated:
                if request.user in obj.liked.all():
                    return True
        except:
            return False
    def get_verb_like(self,obj):
        request = self.context.get("request")
        #user=User.objects.get(pk=request.user.pk)
        like='Like'
        try:
            if request.user.is_authenticated:

                if request.user in obj.liked.all():
                    like='Unlike'
                    return like
        except:
            return like

        return like
            
    def get_likes(self,obj):
        return obj.liked.all().count()

    
    def get_created_at(self,obj):
        return timesince(obj.created_at)+" ago"
    