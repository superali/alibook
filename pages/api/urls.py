       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'pages'
urlpatterns = [
     path('',views.PageList.as_view(),name='list'),
     path('create/', views.PageCreateAPIView.as_view(), name='create'),

    url(r'^(?P<pk>\d+)/like/$', views.LikeToggleView.as_view(), name='like-toggle'),
    url(r'^(?P<pk>\d+)/admin/$', views.AdminToggleView.as_view(), name='admin-toggle'),
    url(r'^(?P<pk>\d+)/admin/(?P<username>[\w.@+-]+)/$', views.AdminRemoveView.as_view(), name='admin-remove'),

    
    
]
