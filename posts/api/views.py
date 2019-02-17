
from rest_framework.response import Response
from rest_framework import generics,mixins
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
from accounts.permissions import IsownerOrReadOnly
from pages.models import Page
from clubs.models import Group
from .serializers import PostModelSerializer,PostUpdateModelSerializer
from accounts.api.serializers import UserDisplaySerializer
from pages.api.serializers import PageModelSerializer
from clubs.api.serializers import GroupDisplaySerializer
from .pagination import StandardResultsPagination

from actions.utils import create_action
    
class PostDetail(mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.ListAPIView):
    serializer_class = PostModelSerializer
    permissions_classes = [IsownerOrReadOnly,]

    def get_queryset(self,*args,**kwargs):
        post_id=self.kwargs.get("pk")
        qs= Post.objects.filter(pk=post_id)
        return qs  
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    def perform_create(self,serializer): 
        content_type=ContentType.objects.get_for_model(User)
        serializer.save(user= self.request.user,content_type=content_type,object_id=self.request.user.pk )
        
class GroupPostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self,serializer): 
        content_type=ContentType.objects.get_for_model(Group)
        serializer.save(user= self.request.user,content_type=content_type,object_id=self.kwargs.get('pk') )
        
class PagePostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    
    def perform_create(self,serializer):
        content_type=ContentType.objects.get_for_model(Page)
        serializer.save(user= self.request.user,content_type=content_type,object_id=self.kwargs.get('pk') )
    
class LikeToggleView(APIView):
    
    def get(self,request,pk,format=None):
  
        post=Post.objects.filter(pk=pk).first()
        if request.user.is_authenticated:
            is_liked= Post.objects.like_toggle(request.user,post)
            if is_liked:
                url='/posts/'+str(post.pk)+'/'
                create_action(request.user,'liked a post By',url,post)
            else:
                url='/posts/'+str(  post.pk)+'/'
                create_action(request.user,'Unliked a post By',url,post) 
            print(url)
            return Response({'liked':is_liked})
        return Response(None,status=400) 

   
class FRequest(APIView):    
    def get(self,request,op,fpk,tpk,format=None):
  
        from_user=User.objects.get(pk=fpk)
        to_user=User.objects.get(pk=tpk)
        if request.user.is_authenticated:
            Profile.objects.friend_request(from_user,to_user,op)
            return Response({'op':op})
        return Response(None,status=400) 



 
class PostListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]

    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):

        op= self.request.GET.get("op")

        pk= self.request.GET.get("pk")
        if op=='profile':
            content_type=ContentType.objects.get_for_model(User)
            queryset=Post.objects.filter(content_type=content_type,object_id=pk)
        elif op=='page':
            content_type=ContentType.objects.get_for_model(Page)
            queryset=Post.objects.filter(content_type=content_type,object_id=pk)
        elif op=='group':
            content_type=ContentType.objects.get_for_model(Group)
            queryset=Post.objects.filter(content_type=content_type,object_id=pk)
        elif op=='home':
            content_type=ContentType.objects.get_for_model(User)
            queryset=Post.objects.filter(content_type=content_type) 

            following_ids = self.request.user.profile.following.values_list('id',flat=True)
            if following_ids:
                queryset=queryset.filter(user_id__in=following_ids)

             
        else:
             queryset=Post.objects.all()[:10]
           


        return queryset

           
class SearchAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get(self,request,format=None):

        if request.user.is_authenticated:
           op= self.request.GET.get("op")

           content= self.request.GET.get("content")
           if op=='users':
               queryset=User.objects.filter(username__icontains=content)
               serializer=UserDisplaySerializer(queryset,many=True)
               return JsonResponse(serializer.data,safe=False)
           elif op=='pages':
               queryset=Page.objects.filter(name__icontains=content)
               serializer=PageModelSerializer(queryset,many=True)
               return JsonResponse(serializer.data,safe=False)           
           elif op=='groups':
               queryset=Group.objects.filter(name__icontains=content)
               serializer=GroupDisplaySerializer(queryset,many=True)
               return JsonResponse(serializer.data,safe=False)             
           elif op=='posts':
               queryset=Post.objects.filter(content__icontains=content)
               serializer=PostModelSerializer(queryset,many=True)
               print(queryset)
               print('queryset')
               return JsonResponse(serializer.data,safe=False)




           else:
                return Response(None,status=400)
           


        return Response(None,status=400)
            
    