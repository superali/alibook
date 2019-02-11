from django.conf import settings
from django.urls import reverse
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from files.models import  Picture

from django.contrib.auth import get_user_model
User=get_user_model()
def upload_Post_image(instance,filename):
    return "posts/{user}/{post}/{filename}".format(user=instance.user,post=instance.id,filename=filename)

class PostManager(models.Manager):

    def imgserialize(self,obj):
        return Picture.objects.all()
    def like_toggle(self,re_user,tweet_obj):
        user=User.objects.get(pk=re_user.pk)
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked
    
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    updated     = models.DateTimeField(auto_now=True)
    liked =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked')

    objects = PostManager()
    def __str__(self):
        return self.content



    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        
