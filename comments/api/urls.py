       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'comments'
urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.CommentDetail.as_view(), name='detail'),

    url(r'^(?P<op>[\w.@+-]+)/(?P<pk>\d+)$', views.CommentListAPIView.as_view(), name='list'),

    url(r'^(?P<pk>\d+)/like/$', views.LikeToggleView.as_view(), name='like-toggle'),

    url(r'^create/(?P<op>[\w.@+-]+)/(?P<pk>\d+)$', views.CommentCreateAPIView.as_view(), name='create'),
 


    
    
]
