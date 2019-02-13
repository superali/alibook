from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.urls import reverse_lazy
from accounts.forms import UserLoginForm,UserSignUpForm
from django.contrib.contenttypes.models import ContentType
from actions.models import Action
from posts.models import Post
from posts.forms import PostCreateForm
User=get_user_model()

class Home(LoginRequiredMixin,ListView):
    template_name='index.html'
    def get_context_data(self,*args,**kwargs):
        context = super(Home,self).get_context_data(*args,**kwargs)
        users =User.objects.exclude(pk=self.request.user.pk)
        friends=self.request.user.profile.friends.all()
        actions = Action.objects.all().exclude(user=self.request.user)
        following_ids = self.request.user.profile.following.values_list('id',flat=True)
        if following_ids:
            actions=actions.filter(user_id__in=following_ids).select_related('user','user__profile').prefetch_related('content_object')
        actions = actions[:10] 
        context['actions'] = actions
        context['post_form'] = PostCreateForm
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        context['users'] = users
        context['friends'] = friends
        return context
    def get_queryset(self):
#        content_type=ContentType.objects.get_for_model(User)
#        obj_id =self.request.user.pk
#        posts=Post.objects.filter(content_type=content_type,object_id=obj_id)
        return None

