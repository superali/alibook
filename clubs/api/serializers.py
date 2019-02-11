from django.utils.timesince import timesince
from rest_framework import serializers

from clubs.models import Group,JoinRequest
from django.contrib.auth import get_user_model
User=get_user_model()
from accounts.api.serializers import UserDisplaySerializer
class GroupDisplaySerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields=[
            'name',
            'pk',
            'members_count',
        ]
    def get_members_count(self,obj):
        return obj.joined.all().count()
class GroupModelSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Group
        fields=[
            'name',
            'pk',
         ]
        
class GroupDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields=[
            'name',
            'pk',
            'members',
        ]
    def get_members(self,obj):
        return obj.joined.all()
    
class RequestModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    group = GroupDisplaySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model=JoinRequest
        fields=[
                'user',
                'created_at',
                'group',
                ]    

    
    def get_created_at(self,obj):
        return timesince(obj.timestamp)+" ago"
    