from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType
import json
from rest_framework import serializers

from chat.models import Message,Conversation
from files.models import Picture
from comments.models import Comment
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer
from files.api.serializers import PictureDisplaySerializer

class MessageModelSerializer(serializers.ModelSerializer):
    from_user = UserDisplaySerializer(read_only=True)
    to_user = UserDisplaySerializer(read_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model=Message
        fields=[
                'id','from_user',
                'content','created',
                'to_user',
                ]
    

    def get_created(self,obj):
        return timesince(obj.created)+" ago"
class ConversationModelSerializer(serializers.ModelSerializer):
    from_user = UserDisplaySerializer(read_only=True)
    to_user = UserDisplaySerializer(read_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model=Conversation
        fields=[
                'id','from_user','from_user_hide',
                'created',
                'to_user', 'to_user_hide',
                ]
    

    def get_created(self,obj):
        return timesince(obj.created)+" ago"
    