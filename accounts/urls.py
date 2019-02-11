from django.urls import path
from django .contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from .forms import UserSignUpForm,UserLoginForm

from . import views
app_name = 'accounts'
urlpatterns = [

    path('signup/',views.SignUp.as_view(),name='signup'),
    path('login/lock/',views.LockPage.as_view(),name='lock'),


    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'
    ,extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,} ),name='login'), 
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}),name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}),
         name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}),name='password_reset_done'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}),name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}), name='password_reset_confirm'),
    
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(extra_context={'login_form':UserLoginForm,'signup_form':UserSignUpForm ,}),name='password_change_done'),
    
        url(r'^(?P<username>[\w.@+-]+)/$',views.ProfileDetailView.as_view(), name='detail'),

]


