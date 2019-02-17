from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
User=get_user_model()

from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import generics
from rest_framework import permissions

from rest_framework.views import APIView
from posts.models import Post
from posts.api.pagination import StandardResultsPagination
from pages.models import Page
from clubs.models import Group
from accounts.models import Profile
from .serializers import PictureDisplaySerializer

from files.models import Picture
from actions.utils import create_action

class LikeToggleView(APIView):
    def get(self,request,pk,format=None):
        post=Picture.objects.filter(pk=pk).first()
        if request.user.is_authenticated:
            is_liked= Picture.objects.like_toggle(request.user,post)
            if is_liked:
                url='/files/'+str(post.pk)+'/'
                create_action(request.user,'liked a picture By',url,post)
            else:
                url='/files/'+str(  post.pk)+'/'
                create_action(request.user,'Unliked a picture By',url,post) 
            return Response({'liked':is_liked})
        return Response(None,status=400) 

   
class FileCreateAPIView(APIView):
    parser_class = (FileUploadParser,)
    
    def post(self,request,op,pk=None,format=None):
        op=self.kwargs.get('op')
        pk=self.kwargs.get('pk')
        print(op)
        if op =='user':
            content_type=ContentType.objects.get_for_model(User)
            object_id=request.user.pk
        elif op =='post':
            content_type=ContentType.objects.get_for_model(Post)
            object_id=pk
        elif op =='page':
            content_type=ContentType.objects.get_for_model(Page)
            object_id=pk
        elif op =='group':
            content_type=ContentType.objects.get_for_model(Group)
            object_id=pk
        if 'file' not in request.data :
            raise ParseError("empty content")
        f=request.data['file']
        if op =='user':
            if request.user ==User.objects.get(pk=pk):
               pic=Picture.objects.create(image=f,user= self.request.user,content_type=content_type,object_id=object_id)
               user=User.objects.get(pk=pk)
               profile=Profile.objects.get(user=user)
               profile.picture=pic.image
               profile.save()
        else:
            Picture.objects.create(image=f,user= self.request.user,content_type=content_type,object_id=object_id)
        serialiser=PictureDisplaySerializer(Picture.objects.filter(content_type=content_type,object_id=object_id),many=True)
        return Response({'img':serialiser.data},status=201) 

  

 
class PhotoList(generics.ListAPIView):
    serializer_class = PictureDisplaySerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self):

        op= self.kwargs.get("op")

        pk= self.kwargs.get("pk")
        if op=='profile':
            content_type=ContentType.objects.get_for_model(User)
            queryset=Picture.objects.filter(content_type=content_type,object_id=pk)
        elif op=='page':
            content_type=ContentType.objects.get_for_model(Page)
            queryset=Picture.objects.filter(content_type=content_type,object_id=pk)

        elif op=='group':
            content_type=ContentType.objects.get_for_model(Group)
            queryset=Picture.objects.filter(content_type=content_type,object_id=pk)

        else:
             queryset=Picture.objects.filter(user=User.objects.get(pk=pk)) 
           


        return queryset

            
    
