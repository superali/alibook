from django.db.models import Q
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from .pagination import RequestResultsPagination,StandardResultsPagination

from .serializers import RequestModelSerializer,GroupDisplaySerializer,GroupModelSerializer
from clubs.models import Group,JoinRequest
class GroupCreateAPIView(generics.CreateAPIView):
    serializer_class = GroupModelSerializer
    
    def perform_create(self,serializer): 
        serializer.save(user= self.request.user )
 
class RequestList(generics.ListAPIView):
    serializer_class = RequestModelSerializer
    pagination_class = RequestResultsPagination
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    def get_queryset(self):

        op= self.request.GET.get("op")

        pk= self.request.GET.get("pk")
        if op=='group':
            group=Group.objects.get(pk=pk)
            user=self.request.user
            if (user == group.user) or(user in group.admins.all()):
                queryset=JoinRequest.objects.filter(group=group)

        return queryset

class AdminToggleView(APIView):
    
    def get(self,request,pk,format=None):       
        group=Group.objects.filter(pk=pk).first()
        admin=User.objects.get(username=request.GET.get('username'))
        if admin :
            if (request.user.is_authenticated and request.user in group.admins.all()) or (request.user.is_authenticated  and request.user == group.user):
                is_admin= Group.objects.admin_toggle(admin,group)
                return Response({'admin':is_admin})
        else:
            pass
        return Response(None,status=400) 
class AdminRemoveView(APIView):
    
    def get(self,request,pk,username,format=None): 
        group=Group.objects.filter(pk=pk).first()
        try:
            admin=User.objects.get(username=username)
        except:
            pass
            
        if admin :
            if (request.user.is_authenticated and request.user in group.admins.all()) or (request.user.is_authenticated  and request.user == page.user):
                is_admin= Group.objects.admin_toggle(admin,group)
                return Response({'admin':is_admin})
        else:
            pass
        return Response(None,status=400) 
class JRequest(APIView):    
    def get(self,request,op,gpk,format=None):
        user=request.user
        group=Group.objects.get(pk=gpk)
        if request.user.is_authenticated:
            Group.objects.join_request(request,user,group,op)
            return Response({'op':op})

        return Response(None,status=400) 

class GroupList(generics.ListAPIView):
    serializer_class = GroupDisplaySerializer
    pagination_class = StandardResultsPagination
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):
        op= self.request.GET.get("op")
        if op=='my':
             queryset=Group.objects.filter((Q(user=self.request.user) )) 
        elif op:
            queryset=Group.objects.filter(name__icontains=op)[:40]

        else:
            queryset=Group.objects.all()[:40]

        return queryset
