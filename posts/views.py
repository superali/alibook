from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages                                       
from django.views import generic
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


from .import models 
from .import forms 
User =get_user_model()

class PostDetail(generic.DetailView):
    model =models.Post
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__iexact=self.kwargs.get('pk'))
                                                                                     
        
                                                                                     
class CreatePost(LoginRequiredMixin,generic.CreateView):
    
    #model =models.Post
    form_class=forms.PostCreateForm
    template_name='posts/create.html'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        content_type=ContentType.objects.get_for_model(User)
        self.object.content_type =content_type
        self.object.user =self.request.user
        self.object.object_id =self.request.user.pk
        self.object.save()
        return super().form_valid(form)   
 