from django.db import models
from django.conf import settings
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
def upload_image(instance,filename):
    return "images/{user}/{image}/{filename}".format(user=instance.user,image=instance.id,filename=filename)

        
class Picture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pics",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)

    image =models.ImageField(upload_to=upload_image,blank=True,null=True) 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    class Meta:
        ordering = ["-created_at"]
        
