       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'files'
urlpatterns = [
    #url(r'^list/(?P<pk>\d+)/(?P<op>[\w.@+-]+)/$', views.PostListAPIView.as_view(), name='list'),
#    url(r'^list/$', views.PostListAPIView.as_view(), name='list'),
#
#    url(r'^(?P<pk>\d+)/like/$', views.LikeToggleView.as_view(), name='like-toggle'),
    url(r'^(?P<pk>\d+)/like/$', views.LikeToggleView.as_view(), name='like-toggle'),
#    
    url(r'^photos/(?P<op>[\w.@+-]+)/(?P<pk>\d+)/$', views.PhotoList.as_view(), name='list'),
    url(r'^create/(?P<op>[\w.@+-]+)/(?P<pk>\d+)/$', views.FileCreateAPIView.as_view(), name='create'),


    
    
]
