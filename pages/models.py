from django.conf import settings
from django.urls import reverse
from django.db import models


#from groups.models import  Group

from django.contrib.auth import get_user_model
User=get_user_model()

class PageManager(models.Manager):

    def admin_toggle(self,re_user,tweet_obj):
        user=User.objects.get(pk=re_user.pk)
        if user:
            if user in tweet_obj.admins.all():
                is_admin = False
                tweet_obj.admins.remove(user)
            else:
                is_admin = True
                tweet_obj.admins.add(user)
            return is_admin
        else:
            return False
    def like_toggle(self,re_user,tweet_obj):
        user=User.objects.get(pk=re_user.pk)
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked
    
class Page(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pages",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60,unique=True)
    content = models.TextField()
    admins =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='admins')

    updated     = models.DateTimeField(auto_now=True)
    liked =   models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='likedpage')
    objects = PageManager()
    #group = models.ForeignKey(Group, related_name="posts",null=True, blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
     
        self.name = self.name.replace(" ","-")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "pages:single",
            kwargs={
                "name": self.name
            }
        )

    class Meta:
        ordering = ["-created_at"]
