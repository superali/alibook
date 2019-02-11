from django.db.models import Q


from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User=get_user_model()
from posts.models import Post
from accounts.models import Profile
from pages.models import Page
from chat.models import Message,Conversation
from .serializers import MessageModelSerializer
from .serializers import ConversationModelSerializer
from accounts.api.serializers import UserDisplaySerializer
from pages.api.serializers import PageModelSerializer
from clubs.api.serializers import GroupDisplaySerializer
from .pagination import StandardResultsPagination
from chat.utils import create_conversation
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageModelSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self,serializer): 
        pk =  self.kwargs.get('pk')
        to_user=User.objects.get(pk=pk)
        serializer.save(to_user= to_user,from_user=self.request.user )
        create_conversation(self.request.user,to_user)
        
       
class MessageList(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]

    serializer_class = MessageModelSerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):
        pk= self.kwargs.get("pk")
        queryset=Message.objects.filter(to_user=self.request.user).distinct()[:10]
 
        return queryset
 
class ConversationListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationModelSerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):

        queryset=Conversation.objects.filter((Q(from_user=self.request.user)|
                                                      Q(to_user=self.request.user)))


        return queryset

class ConversationAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = MessageModelSerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):

        fusername= self.kwargs.get("fusername")
        tusername= self.kwargs.get("tusername")
        queryset=Message.objects.filter(Q(
                                                      Q(from_user__username=fusername)&
                                                      Q(to_user__username=tusername)
                                        )|Q(
                                                      Q(to_user__username=fusername)&
                                                      Q(from_user__username=tusername)
                                        )
                                       )


        return queryset

         