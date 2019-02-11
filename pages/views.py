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

from .models import Page 
from .import forms 
User =get_user_model()
class PageDetailView(DetailView):
    model=Page
    def get_object(self):

        obj = cache.get('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("name")),None)
        if not obj:
            qs=Page.objects.filter(name=self.kwargs.get("name"))
            print(qs)
            if qs.exists():
                obj=qs.first()
                cache.set('%s-%s'%(self.model.__name__.lower(),self.kwargs.get("name")),obj)
            else:
                return None
        return obj
    def get_context_data(self,*args,**kwargs):
        context = super(PageDetailView,self).get_context_data(*args,**kwargs)
        content_type=ContentType.objects.get_for_model(Page)
        obj_id =(Page.objects.get(name=self.kwargs.get("name"))).pk

        posts=Post.objects.filter(content_type=content_type,object_id=obj_id)
        context['post_form'] = PostCreateForm
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        context['posts'] = posts
        return context
class MyPageList(ListView):
    model=Page
    def get_queryset(self):
        qs=Page.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self,*args,**kwargs):
        context = super(MyPageList,self).get_context_data(*args,**kwargs)
        context['login_form'] = UserLoginForm
        context['signup_form'] = UserSignUpForm
        return context

    
                                                                                     
class CreatePage(LoginRequiredMixin,CreateView):
    
    #model =models.Post
    form_class=forms.PageCreateForm
    template_name='pages/create.html'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user =self.request.user
        self.object.save()
        return super().form_valid(form)   
class CreatePagePost(LoginRequiredMixin,CreateView):
    
    #model =models.Post
    form_class=PostCreateForm
    template_name='pages/post_create.html'
    def form_valid(self,form):
        page=Page.objects.get(name=self.kwargs.get("name"))
        if self.request.user==page.user or self.request.user in page.admins.all():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            content_type=ContentType.objects.get_for_model(Page)
            self.object.content_type =content_type
            self.object.object_id =(Page.objects.get(name=self.kwargs.get("name"))).pk
            self.object.save()
        else:
            pass
        return super().form_valid(form)   
 