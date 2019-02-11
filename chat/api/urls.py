       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'chat'
urlpatterns = [
    path('list/',views.MessageList.as_view(),name='list'),
   url(r'^list/cons/$', views.ConversationListAPIView.as_view(), name='cons'),
   url(r'^conversation/(?P<fusername>[\w.@+-]+)/(?P<tusername>[\w.@+-]+)/$', views.ConversationAPIView.as_view(), name='con'),
#    url(r'^list/$', views.PostListAPIView.as_view(), name='list'),
#    path('search/', views.SearchAPIView.as_view(), name='search'),
#
    url(r'^create/(?P<pk>\d+)/$', views.MessageCreateView.as_view(), name='create'),
#    url(r'^(?P<op>[\w.@+-]+)/(?P<fpk>\d+)/(?P<tpk>\d+)/$',views.FRequest.as_view(), name='frequest'),
#    
#        path('create/', views.PostCreateAPIView.as_view(), name='create'),
#        url(r'^create/page/(?P<pk>\d+)/$', views.PagePostCreateAPIView.as_view(), name='page'),
#         url(r'^create/group/(?P<pk>\d+)/$', views.GroupPostCreateAPIView.as_view(), name='group'),


    
    
]