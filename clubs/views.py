from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages                                       
from django.views.generic import DetailView,CreateView,ListView
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from posts.forms import PostCreateForm
from accounts.forms import UserLoginForm,UserSignUpForm
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .models import Group ,JoinRequest
from .import forms 
from django.utils.translation import gettext as _

class CreateGroup(LoginRequiredMixin,CreateView):
    form_class=forms.GroupCreateForm
    template_name='clubs/create.html'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user =self.request.user
        self.object.save()
        return super().form_valid(form)  
    def get_context_data(self,*args,**kwargs):
        context = super(CreateGroup,self).get_context_data(*args,**kwargs)
        context['post_form'] = PostCreateForm
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        return context    
class GroupDetailView(DetailView):
    model=Group
    def get_object(self):

        obj = cache.get('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("name")),None)
        if not obj:
            qs=Group.objects.filter(name=self.kwargs.get("name"))
            if qs.exists():
                obj=qs.first()
                cache.set('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("name")),obj)
            else:
                return None
        return obj
    def get_context_data(self,*args,**kwargs):
        context = super(GroupDetailView,self).get_context_data(*args,**kwargs)
        if JoinRequest.objects.filter(user=self.request.user,group=self.object):
            status='Cancel Join Request'
            op='cancel'

        elif self.request.user in self.object.joined.all():
            status='Leave Group'
            op='delete'
        else :
                status='Join'
                op='send'
        #posts=Post.objects.filter(content_type=content_type,object_id=obj_id)
        context['op'] = op
        context['status'] = status
        context['post_form'] = PostCreateForm
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        #context['posts'] = posts
        return context
class MyGroupList(LoginRequiredMixin,ListView):
    def get_queryset(self):
        qs=Group.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self,*args,**kwargs):
        context = super(MyGroupList,self).get_context_data(*args,**kwargs)
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        return context

       
class CreateGroupPost(LoginRequiredMixin,CreateView):
    
    #model =models.Post
    form_class=PostCreateForm
    template_name='clubs/post_create.html'
    def form_valid(self,form):
        group=Group.objects.get(name=self.kwargs.get("name"))
        if self.request.user in group.joined.all() or self.request.user==group.user:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            content_type=ContentType.objects.get_for_model(Group)
            self.object.content_type =content_type
            self.object.object_id =group.pk
            self.object.save()
        else:
            raise ValidationError(_("your are not a member of {}".format(group.name)))
        return super().form_valid(form)   
 