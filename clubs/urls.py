from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'clubs'
urlpatterns = [
    #path('',views.ListGroup.as_view(),name='all'),
    path('',views.MyGroupList.as_view(),name='mylist'),
    path('new/add',views.CreateGroup.as_view(),name='create'),
    url(r'^(?P<name>[\w.@+-]+)/$',views.GroupDetailView.as_view(), name='single'),
       url(r'^post/(?P<name>[\w.@+-]+)/$',views.CreateGroupPost.as_view(), name='post'),
 
   # url(r'^join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
    #url(r'^leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
]
