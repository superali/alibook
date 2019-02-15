from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
User= get_user_model()
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,re,data ):
        username = data.get("username","")
        password = data.get("password","")
        if username and password :
            user = authenticate(username=username, password=password,request = re)
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    msg='account deactivated'
                    raise exceptions.validationError(msg)
            else:
                msg='unable to login with given credintials'
                raise exceptions.validationError(msg)
        else:
            msg='Must provide both username and password'
            raise exceptions.validationError(msg)
        return data
class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('username', 'email', 'password')

         extra_kwargs = {'password': {'write_only': True}}
     def create(self, validated_data):
         user = User(
         email=validated_data['email'],
         username=validated_data['username'])
         user.set_password(validated_data['password'])
         user.save()
         Token.objects.create(user=user)
         return user
class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=[
            'id',
            'username',
            'first_name',
            'last_name',
            'last_name',

        ]
'''    def get_followers_count(self,obj):
        return 0
    def get_url(self,obj):
        return reverse_lazy("accounts:profile",kwargs={"username":obj.username})
    
'''