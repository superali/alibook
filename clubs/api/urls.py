       
# Create your views here.
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'clubs'
urlpatterns = [
     path('',views.GroupList.as_view(),name='list'),

    path('create/', views.GroupCreateAPIView.as_view(), name='create'),
    url(r'^requests/$', views.RequestList.as_view(), name='request-list'),
    url(r'^(?P<pk>\d+)/admin/$', views.AdminToggleView.as_view(), name='admin-toggle'),
    url(r'^(?P<pk>\d+)/admin/(?P<username>[\w.@+-]+)/$', views.AdminRemoveView.as_view(), name='admin-remove'),
    url(r'^(?P<op>[\w.@+-]+)/(?P<gpk>\d+)/$',views.JRequest.as_view(), name='jrequest'),


    
    
]
