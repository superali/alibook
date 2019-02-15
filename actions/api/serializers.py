from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType
import json
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from actions.models import Action
from clubs.models import Group
from clubs.api.serializers import GroupModelSerializer
from posts.api.serializers import PostModelSerializer
from posts.models import Post
from pages.models import Page
from comments.models import Comment
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer

class GenericRelatedField(ReadOnlyField):
    read_only = False
    _default_view_name = '%(model_name)s-detail'
    lookup_field = 'pk'
    def __init__(self,related_models=(),**kwargs):
        super(GenericRelatedField,self).__init__(kwargs)
class ObjectRelatedField(serializers.ReadOnlyField):
    def to_representaion(self,value):
        if isinstance(value,User):
            return 'User:'+value.username
        elif isinstance(value,Post):
            serializer = PostModelSerializer(value)
        elif isinstance(value,Group):
            serializer = GroupModelSerializer(value)
        elif isinstance(value,Page):
            return 'Page:'+value.name
        elif isinstance(value,Comment):
            serializer = CommentModelSerializer(value)
        raise Exception('Unexpected type of object type')
        
class ActionModelSerializer(serializers.HyperlinkedModelSerializer):
    user = UserDisplaySerializer(read_only=True)
#    content_object = GenericRelatedField(related_models=(Post,Comment,User,Page,Group))
    content_object = ObjectRelatedField()
    created = serializers.SerializerMethodField()
    class Meta:
        model=Action
        fields=[
                'id','user',
                'verb','created','content_object',
                 ]
    

    def get_created(self,obj):
        return timesince(obj.created)+" ago"
    