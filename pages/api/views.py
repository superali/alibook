
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User=get_user_model()
from pages.models import Page
from  .serializers import PageModelSerializer
from  .pagination import StandardResultsPagination
from actions.utils import create_action
class PageCreateAPIView(generics.CreateAPIView):
    serializer_class = PageModelSerializer
    
    def perform_create(self,serializer): 
        serializer.save(user= self.request.user )
       
class LikeToggleView(APIView):
    
    def get(self,request,pk,format=None):
  
        page=Page.objects.filter(pk=pk).first()
        if request.user.is_authenticated:
            is_liked= Page.objects.like_toggle(request.user,page)
            create_action(request.user,'likes',page)
            return Response({'liked':is_liked})
        return Response(None,status=400) 
class AdminToggleView(APIView):
    
    def get(self,request,pk,format=None):       
        page=Page.objects.filter(pk=pk).first()
        try:
            admin=User.objects.get(username=request.GET.get('username'))
        except:

            admin= request.user
            
        if admin :
            if (request.user.is_authenticated and request.user in page.admins.all()) or (request.user.is_authenticated  and request.user == page.user):
                is_admin= Page.objects.admin_toggle(admin,page)
                return Response({'admin':is_admin})
        else:
            pass
        return Response(None,status=400) 
class AdminRemoveView(APIView):
    
    def get(self,request,pk,username,format=None): 
        page=Page.objects.filter(pk=pk).first()
        try:
            admin=User.objects.get(username=username)
        except:

            admin= request.user
            
        if admin :
            if (request.user.is_authenticated and request.user in page.admins.all()) or (request.user.is_authenticated  and request.user == page.user):
                is_admin= Page.objects.admin_toggle(admin,page)
                return Response({'admin':is_admin})
        else:
            pass
        return Response(None,status=400) 


 
class PageList(generics.ListAPIView):
    serializer_class = PageModelSerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):
        op= self.request.GET.get("op")
        if op=='my':
            queryset=Page.objects.filter(user=self.request.user)
        elif op:
            queryset=Page.objects.filter(name__icontains=op)[:40]

        else:
            queryset=Page.objects.all()[:40]

        return queryset

         