from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='actions',db_index=True)
    verb = models.CharField(max_length = 255)
    url = models.CharField(blank=True,null=True,max_length = 255)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=True,null=True)
    object_id = models.PositiveIntegerField(blank=True,null=True)
    content_object = GenericForeignKey('content_type','object_id')   
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    def __str__(self):
        return self.user.username+" "+self.verb


    class Meta:
        ordering = ["-created"]
        
