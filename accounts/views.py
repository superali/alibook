
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from accounts.forms import UserLoginForm,UserSignUpForm
from accounts.models import FriendRequest
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from posts.forms import PostCreateForm


from django.contrib.auth import authenticate, login
from django.views.generic import CreateView,TemplateView,DetailView,ListView
from django.contrib import messages
from django.urls import reverse_lazy
#from search.forms import SearchForm
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model

from .import forms 
from .models import Profile 
# Create your views here.
User=get_user_model()   
class LockPage(TemplateView):
    template_name = 'lock.html'
    def get_context_data(self,*args,**kwargs):
        context = super(LockPage,self).get_context_data(*args,**kwargs)
        context['login_form'] = forms.UserLoginForm
        context['signup_form'] = forms.UserSignUpForm
        return context

        return context
class SignUp(CreateView):
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'



class ProfileDetailView(LoginRequiredMixin,DetailView):
    model=Profile
    def get_object(self):
        obj = cache.get('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("username")),None)
        if not obj:
            qs=Profile.objects.filter(user__username=self.kwargs.get("username"))
            if qs.exists():
                obj=qs.first()
                cache.set('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("username")),obj)
            else:
                pass
        return obj

    def get_context_data(self,*args,**kwargs):
        context = super(ProfileDetailView,self).get_context_data(*args,**kwargs)
        content_type=ContentType.objects.get_for_model(User)
        #username=self.kwargs.get('username')
        #user=User.objects.filter(username=username).first()
        status='none'
        op='none'
        if self.object:
            pk=self.object.user.pk
            sent_frequests=FriendRequest.objects.filter(from_user=self.object.user)
            res_frequests=FriendRequest.objects.filter(to_user=self.object.user)
            friends=self.object.friends.all()

            if FriendRequest.objects.filter(from_user=self.request.user,to_user=self.object.user):
                status='Cancel Friend Request'
                op='cancel'
            elif FriendRequest.objects.filter(to_user=self.request.user,from_user=self.object.user):
                status='Confirm Friend Request'
                op='confirm'
            elif self.request.user.profile in friends:
                status='UnFriend'
                op='delete'
            else :
                status='Add Friend'
                op='send'

            context['friends'] = friends
            if self.request.user==self.object.user:
                context['sent_frequests'] = sent_frequests
                context['res_frequests'] = res_frequests 

            posts=Post.objects.filter(content_type=content_type,object_id=pk)
            context['posts'] = posts
        context['post_form'] = PostCreateForm
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        context['status'] = status
        context['op'] = op
        
          

        return context


           
