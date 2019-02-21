from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Message(models.Model):
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_message',db_index=True)    
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='rec_message',db_index=True) 
    content = models.CharField(max_length = 255)

    created = models.DateTimeField(auto_now=True,db_index=True)
    def __str__(self):
        return self.from_user.username+" to "+self.to_user.username


    class Meta:
        ordering = ["-created"]
        
class ConversationManager(models.Manager):

#    def message_add(self,msg,con):
#        if msg in con.messages.all():
#            con.messages.remove(user)
#        else:
#            con.messages.add(msg)
#        return con    
    def message_add(self,msg,con):
        if msg in con.messages.all():
            return con
        else:
            con.messages.add(msg)
        return con    
    def message_remove(self,msg,con):
        if msg in con.messages.all():
            con.messages.remove(msg)
        else:
            return con
        return con
class Conversation(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_conversatons',db_index=True)    
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='rec_conversatons',db_index=True)   
    created = models.DateTimeField(auto_now=True,db_index=True)
    to_user_hide = models.CharField(max_length = 70,default='show',null=True,blank=True)
    from_user_hide = models.CharField(max_length = 70,default='show',null=True,blank=True)

    messages =   models.ManyToManyField(Message,blank=True,null=True,related_name='messages')
    objects=ConversationManager()
    def __str__(self):
        return self.from_user.username+" to "+self.to_user.username


    class Meta:
        ordering = ["-created"]
        
