from django.conf.urls import url
from .views import UserFollowView,LoginView,SignupView
from django.urls import path
app_name = 'accounts'

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/follow/$',UserFollowView.as_view(), name='follow'),

    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),


    
]