from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from comments.models import Comment
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer

class CommentModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    verb_like = serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=[
                'id','user',
                'content','created_at',
                'likes','did_like','verb_like','comment_count',
                ]
    
    def get_did_like(self,obj):
        request = self.context.get("request")
        #user=User.objects.get(pk=request.user.pk)
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

    def get_comment_count(self,obj):
        content_type=ContentType.objects.get_for_model(Comment)
        return Comment.objects.filter(content_type=content_type,object_id=obj.id).count() 
        
    def get_created_at(self,obj):
        return timesince(obj.created_at)+" ago"
    