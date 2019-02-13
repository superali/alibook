from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from actions.utils import create_action
User=get_user_model()
from django.contrib.auth import authenticate
from .serializers import UserSerializer
class SignupView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer
  
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print(request.data)
        user = authenticate(username=username, password=password,request=request)
        if user:
           return Response({"token": user.auth_token.key })
        else:
           return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
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
  