       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'pages'
urlpatterns = [
     path('',views.MyPageList.as_view(),name='mylist'),
    path('new/',views.CreatePage.as_view(),name='create'),
#    url(r'^by/(?P<username>[-\w]+)',views.UserPosts.as_view(),name='for_user'),
    url(r'^post/(?P<name>[\w.@+-]+)/$',views.CreatePagePost.as_view(), name='post'),
    url(r'^(?P<name>[\w.@+-]+)/$',views.PageDetailView.as_view(), name='single'),

#    url(r'^delete/(?P<pk>\d+)/$',views.DeletePost.as_view(),name='delete'),
    
    
]
