from django.db import models
from django.conf import settings
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
def upload_image(instance,filename):
    return "images/{user}/{image}/{filename}".format(user=instance.user,image=instance.id,filename=filename)

class PictureManager(models.Manager):
    def like_toggle(self,re_user,pic):
        user=User.objects.get(pk=re_user.pk)
        if user in pic.liked.all():
            is_liked = False
            pic.liked.remove(user)
        else:
            is_liked = True
            pic.liked.add(user)
        return is_liked
            
class Picture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pics",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    liked =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked_picture')

    image =models.ImageField(upload_to=upload_image,blank=True,null=True) 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    objects=PictureManager()
    class Meta:
        ordering = ["-created_at"]
        
