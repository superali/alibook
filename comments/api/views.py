from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User=get_user_model()
from posts.models import Post
from comments.models import Comment
from pages.models import Page
from clubs.models import Group
from .serializers import CommentModelSerializer
from .pagination import StandardResultsPagination
from actions.utils import create_action
    
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentModelSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self,serializer): 
        op =  self.kwargs.get('op')
        pk =  self.kwargs.get('pk')
        if op =='comment':
            print(op)
            content_type=ContentType.objects.get_for_model(Post)
        else:
            print(op)
            content_type=ContentType.objects.get_for_model(Comment)

        serializer.save(user= self.request.user,content_type=content_type,object_id=pk )
        
        
        
    
class LikeToggleView(APIView):
    
    def get(self,request,pk,format=None):
  
        comment=Comment.objects.get(pk=pk)
        if request.user.is_authenticated:
            is_liked= Comment.objects.like_toggle(request.user,comment)
            create_action(request.user,'likes',comment)

            return Response({'liked':is_liked})
        return Response(None,status=400) 

    

 
class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentModelSerializer
    pagination_class = StandardResultsPagination
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):

        op= self.kwargs.get("op")

        pk= self.kwargs.get("pk")
        if op=='comment':
            content_type=ContentType.objects.get_for_model(Post)

            queryset=Comment.objects.filter(content_type=content_type,object_id=pk)
        elif op=='reply':
            content_type=ContentType.objects.get_for_model(Comment)
            queryset=Comment.objects.filter(content_type=content_type,object_id=pk)

        else:
             queryset=Comment.objects.all()
           


        return queryset

            
    