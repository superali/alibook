from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from clubs.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
User=get_user_model()

def upload_Profile_image(instance,filename):
    return "profile/{user}/{profile}/{filename}".format(user=instance.user.username,profile=instance.profile.id,filename=filename)
class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have an username') 
        if not password:
            raise ValueError('User must have password')
        user = self.model(
        email=self.normalize_email(email),
        username=self.normalize_username(username),
        )
        user.set_password(password)
        user.active=is_active
        user.admin=is_admin
        user.staff=is_staff
        user.save(using=self._db)
        return user
    def create_staffuser(self,username,email,password=None):
        use=self.create_user(email=email,username=username,password=password,is_staff=True)
        return user
    def create_superuser(self,username,email,password=None):
        use=self.create_user(email=email,username=username,password=password,is_staff=True,is_admin=True)
        return user
class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    active  = models.BooleanField(default=True)
    staff  = models.BooleanField(default=False)
    admin  = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    
    objects=UserManager()
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.admin    
    @property
    def is_active(self):
        return self.active    
    @property
    def is_staff(self):
        return self.staff
class ProfileManager(models.Manager):
    def all(self):
        qs=self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs
    def toggle_follow(self,user,toggle_user):
        
        
        userProfile=Profile.objects.get(user=user)
            
        if toggle_user in userProfile.following.all():
            userProfile.following.remove(toggle_user) 
            added = False
        else:
            userProfile.following.add(toggle_user)
            added = True
        return added
    def is_following(self,user,followed_by_user):
        userProfile=Profile.objects.get(user=user)
        if followed_by_user in userProfile.following.all():
            return True
        return False

        
        
    def friend_request(self,from_user,to_user,op):
        if op =='send':
            frequest,created = FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
            self.toggle_follow(from_user,to_user)
        if op =='cancel':
            frequest = FriendRequest.objects.filter(from_user=from_user,to_user=to_user).first()
            if from_user==frequest.from_user:
                frequest.delete()
        if op =='confirm':
            frequest = FriendRequest.objects.filter(from_user=to_user,to_user=from_user).first()
            self.toggle_follow(to_user,from_user)
            from_user.profile.friends.add(to_user.profile)
            to_user.profile.friends.add(from_user.profile)
            frequest.delete()
            
        if op =='delete':
            from_user.profile.friends.remove(to_user.profile)
            to_user.profile.friends.remove(from_user.profile)
                
             
class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete="CASCADE")
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="followed_by",symmetrical=False)

    friends=models.ManyToManyField('Profile',blank=True)
    picture = models.ImageField(upload_to=upload_Profile_image,blank=True,null=True) 
    objects=ProfileManager()

    
    def __str__(self):
        return "{}".format(self.user.username)
 
    def get_absolute_url(self):
        return reverse("detail", kwargs={"name": self.user.username,
                })
    

        
    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)
        cache.delete('profile-%s'% self.user.username)
        
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
    
class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user',on_delete='CASCADE')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='from_user',on_delete='CASCADE')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "From{},to {}".format(self.from_user.username,self.to_user.username)
    

    