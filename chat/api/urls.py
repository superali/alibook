       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'chat'
urlpatterns = [
    path('list/',views.MessageList.as_view(),name='list'),
   url(r'^list/cons/$', views.ConversationListAPIView.as_view(), name='cons'),
   url(r'^conversation/(?P<fusername>[\w.@+-]+)/(?P<tusername>[\w.@+-]+)/$', views.ConversationAPIView.as_view(), name='con'),
   url(r'^con/delete/(?P<pk>\d+)/hide/$', views.ConversationDeleteAPIView.as_view(), name='con_delete'),

#
    url(r'^create/(?P<pk>\d+)/$', views.MessageCreateView.as_view(), name='create'),
    url(r'^delete/(?P<pk>\d+)/$', views.MessageDeleteView.as_view(), name='delete'),


    
    
]