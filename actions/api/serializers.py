from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType
import json
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from actions.models import Action
from clubs.models import Group
from clubs.api.serializers import GroupModelSerializer
from posts.api.serializers import PostModelSerializer
from files.api.serializers import PictureDisplaySerializer
from comments.api.serializers import CommentModelSerializer
from posts.models import Post
from pages.models import Page
from comments.models import Comment
from files.models import Picture
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer


class ObjectRelatedField(serializers.RelatedField):
    def to_representation(self,value):
        if isinstance(value,User):
            return  value.username
        elif isinstance(value,Post):
            return value.user.username
        elif isinstance(value,Group):
            return 'in'+value.name
        elif isinstance(value,Page):
            return  value.name
        elif isinstance(value,Comment):
            return value.user.username
        elif isinstance(value,Picture):
            return value.user.username
        else:
            raise Exception('Unexpected type of object type {}'.format(value))
        return serializer.data
        
class ActionModelSerializer(serializers.HyperlinkedModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    content_object = ObjectRelatedField(read_only=True)
    created = serializers.SerializerMethodField()
    class Meta:
        model=Action
        fields=[
                'id','user','url',
                'verb','created','content_object',
                 ]
    

    def get_created(self,obj):
        return timesince(obj.created)+" ago"
    