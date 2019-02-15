from django.conf.urls import url
from .views import UserFollowView,LoginView,SignupView,LogoutView
from django.urls import path
app_name = 'accounts'

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/follow/$',UserFollowView.as_view(), name='follow'),

    path('logout/',LogoutView.as_view(),name='logout'),
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),


    
]