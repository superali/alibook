
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import JsonResponse

from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User=get_user_model()
 
from actions.models import Action
from .serializers import ActionModelSerializer
from .pagination import StandardResultsPagination

class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionModelSerializer
    pagination_class = StandardResultsPagination
    permissions_classes = [permissions.IsAuthenticated]
   
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context
    def get_queryset(self):

        op= self.request.GET.get("op")

        pk= self.request.GET.get("pk")
        
        actions = Action.objects.all().exclude(user=self.request.user)
        following_ids = self.request.user.profile.following.values_list('id',flat=True)
        if following_ids:
            actions=actions.filter(user_id__in=following_ids).select_related('user','user__profile').prefetch_related('content_object')
        actions = actions[:10]
        
        return actions
#class ActionListAPIView(APIView):
#    pagination_class = StandardResultsPagination
#    permissions_classes = [permissions.IsAuthenticated]
#
#    def get(self,request,format=None):
#
#        op= self.request.GET.get("op")
#
#        pk= self.request.GET.get("pk")
#        
#        actions = Action.objects.all().exclude(user=self.request.user)
#        following_ids = self.request.user.profile.following.values_list('id',flat=True)
#        if following_ids:
#            actions=actions.filter(user_id__in=following_ids).select_related('user','user__profile').prefetch_related('content_object')
#        actions = actions[:10]
#        serializer=serializers('xml',User.objects.all(),many=True)
#        serializer=serializers('json',Action.objects.all())
#        return JsonResponse(serializer.data,safe=False)       
##        return actions
