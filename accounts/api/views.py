from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication   import TokenAuthentication
from rest_framework import exceptions

from rest_framework.response import Response
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model,login,logout
from actions.utils import create_action
User=get_user_model()
from django.contrib.auth import authenticate
from .serializers import UserSerializer,PasswordChangeSerializer
class ChangePasswordView(generics.CreateAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self,request,*args,**kwargs):

        user = get_object_or_404(User,username=request.user.username)
        user.set_password(request.data.get('password'))
        print('pppppppppppp')
        print(request.data.get('password'))
        print(request.data )
        user.save()
        return Response({'detail':'Password has been changed'})

class SignupView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer
  
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password :
            user = authenticate(username=username, password=password,request = request)
            if not user:
                user = authenticate(email=username, password=password,request = request)
            if user:
                if user.is_active:
                    pass
                else:
                    msg='account deactivated'
                    raise exceptions.ValidationError(msg)
            else:
                msg='unable to login with given credintials'
                raise exceptions.ValidationError(msg)
        else:
            msg='Must provide both username and password'
            raise exceptions.ValidationError(msg)
        login(request,user)
        token,cr=Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=200)

    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)

        return Response( status=204)
 
 
class UserFollowView(APIView):
    def get(self,request,username,*args,**kwargs):
        toggle_user = get_object_or_404(User,username=username)
        if request.user.is_authenticated:
            is_following=Profile.objects.toggle_follow(request.user,toggle_user)
            if is_following:
                followStatus='Unfollow'

            else:
                 followStatus='Follow'
            url='accounts/'+toggle_user.username+'/'
            create_action(request.user,followStatus+'ed You',url,toggle_user)

            return Response({'followStatus':followStatus})
        return Response(None,status=400) 
  