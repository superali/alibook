from django.conf import settings
from django.urls import reverse
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from groups.models import  Group

from django.contrib.auth import get_user_model
User=get_user_model()

class CommentManager(models.Manager):

    def like_toggle(self,re_user,comment_obj):
        user=User.objects.get(pk=re_user.pk)
        if user in comment_obj.liked.all():
            is_liked = False
            comment_obj.liked.remove(user)
        else:
            is_liked = True
            comment_obj.liked.add(user)
        return is_liked
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    updated     = models.DateTimeField(auto_now=True)
    liked =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked_comment')

    objects = CommentManager()
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
        
