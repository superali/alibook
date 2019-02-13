"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .import views
from ang.views  import  AngularTemplateView
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    path('admin/', admin.site.urls),

    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('posts/',include('posts.urls',namespace='posts')),
    path('api/posts/',include('posts.api.urls',namespace='posts-api')),
    path('api/actions/',include('actions.api.urls',namespace='actions-api')),
    path('api/accounts/',include('accounts.api.urls',namespace='accounts-api')),
    path('api/chat/',include('chat.api.urls',namespace='chat-api')),
    path('api/pages/',include('pages.api.urls',namespace='pages-api')),
    path('api/comments/',include('comments.api.urls',namespace='comments-api')),
    path('api/groups/',include('clubs.api.urls',namespace='groups-api')),
    path('api/files/',include('files.api.urls',namespace='files-api')),
    path('pages/',include('pages.urls',namespace='pages')),
    path('groups/',include('clubs.urls',namespace='groups')),
    #path('api/posts/', include('posts.api.urls',namespace='posts-api')),

    path('',views.Home.as_view(),name='home'),
    path('temp/',TemplateView.as_view(template_name='ang/home.html')),
    url(r'api/templates/(?P<name>[A-Za-z0-9\_\-\.\/]+)/(?P<item>[A-Za-z0-9\_\-\.\/]+)\.html$',AngularTemplateView.as_view()),
]
if settings.DEBUG :
#    import debug_toolbar
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)    
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
   #urlpatterns +=url(r'^__debug__/',include(debug_toolbar.urls)),
    
