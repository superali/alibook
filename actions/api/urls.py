       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'actions'
urlpatterns = [
    url(r'^list/$', views.ActionListAPIView.as_view(), name='list'),

#    url(r'^(?P<pk>\d+)/like/$', views.LikeToggleView.as_view(), name='like-toggle'),
#    url(r'^(?P<op>[\w.@+-]+)/(?P<fpk>\d+)/(?P<tpk>\d+)/$',views.FRequest.as_view(), name='frequest'),
#    
#        path('create/', views.PostCreateAPIView.as_view(), name='create'),
#        url(r'^create/page/(?P<pk>\d+)/$', views.PagePostCreateAPIView.as_view(), name='page'),
#         url(r'^create/group/(?P<pk>\d+)/$', views.GroupPostCreateAPIView.as_view(), name='group'),
#
#
#    
    
]
