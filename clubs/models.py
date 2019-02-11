 
from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth import get_user_model
from django import template
from actions.utils import create_action
# Create your models here.
User = get_user_model()

class GroupManager(models.Manager):

    def admin_toggle(self,re_user,group):
        #user=User.objects.get(pk=re_user.pk)
        if re_user:
            if re_user in group.admins.all():
                is_admin = False
                group.admins.remove(re_user)
            else:
                is_admin = True
                group.admins.add(re_user)
            return is_admin
        else:
            return False
        
    def join_request(self,request,user,group,op):

        if op =='send':
            frequest,created = JoinRequest.objects.get_or_create(user=user,group=group)
            create_action(user,'Sent Join Request To {}'.format(group.name),group)
        if op =='cancel':
            frequest = JoinRequest.objects.filter(user=user,group=group).first()

            if user==frequest.user:
                frequest.delete()
        if op =='confirm':
            frequest = JoinRequest.objects.filter(user=user,group=group).first()
            if request.user in group.admins.all() or request.user == group.user:
                if user in group.joined.all():
                    is_joined = False
                    group.joined.remove(user)
                else:
                    is_joined = True
                    group.joined.add(user)
            create_action(user,'{} have approved your  Request To Join {} '.format(user.username,group.name),group)

            frequest.delete()
            
        if op =='delete':
            if request.user in group.admins.all() or request.user == group.user or request.user in group.joined.all() :
                frequest = JoinRequest.objects.filter(user=user,group=group).first()
                if user in group.joined.all():
                    
                    is_joined = False
                    group.joined.remove(user)
                    
                
                elif user ==frequest.user:
                    frequest.delete()
        

                    
        return op
    def join_toggle(self,re_user,tweet_obj):
        user=User.objects.get(pk=re_user.pk)
        if user in tweet_obj.joined.all():
            is_joined = False
            tweet_obj.joined.remove(user)
        else:
            is_joined = True
            tweet_obj.joined.add(user)
        return is_joined

    
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="clubs",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    approved     = models.BooleanField(default=True)
    joined =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='joingroup')
    admins =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='admin')

    objects = GroupManager()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ","-")
        try:
            if self.user not in self.joined.all():
                self.joined.add(self.user)
        except:
            pass
            
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("clubs:single", kwargs={"name": self.name})


    class Meta:
        ordering = ["name"]

class JoinRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user',on_delete='CASCADE')
    group = models.ForeignKey(Group,related_name='group',on_delete='CASCADE')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "From {},to {}".format(self.user.username,self.group.name)
    